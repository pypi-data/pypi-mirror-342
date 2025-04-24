import re
from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from bigdata_client.exceptions import BigdataClientError
from bigdata_client.models.chat import Chat
from bigdata_client.models.chat import ChatInteraction as ChatInteractionModel
from bigdata_client.models.chat import ChatScope, ChatSource, InlineAttributionFormatter


def parse_audit_traces(audit_traces) -> list[ChatSource]:
    sources = []
    for json_data in audit_traces:

        if "results" not in json_data:
            continue

        for result in json_data["results"]:
            result_type = result.get("type")
            values = result.get("values", [])

            if result_type == "EXTERNAL":
                for value in values:
                    action = value.get("action", {})
                    attribution = ChatSource(
                        id=value.get("id", ""),
                        headline=value.get("hd", ""),
                        url=action.get("url"),
                        document_scope=None,
                        rp_provider_id=None,
                    )
                    sources.append(attribution)

            elif result_type == "CQS":
                for value in values:
                    attribution = ChatSource(
                        id=value.get("id", ""),
                        headline=value.get("hd", ""),
                        url=value.get("url"),
                        document_scope=value.get("documentScope"),
                        rp_provider_id=value.get("rpProviderId"),
                    )
                    sources.append(attribution)

    return sources


class ReferenceParser:
    def __init__(
        self,
        sources,
        formatter: InlineAttributionFormatter,
    ):
        self.sources = sources
        self.formatter = formatter

    @staticmethod
    def _parse_ref_list(value: str) -> list:
        match = re.findall(r"\[([A-Z]+:[\w\d-]+)\]", value)
        return match

    @staticmethod
    def _extract_cqs_id(value: str) -> str:
        match = re.search(r":(\w+)-", value)
        return match.group(1) if match else ""

    @staticmethod
    def _extract_external_id(value: str) -> str:
        match = re.search(r":(\w+)", value)
        return match.group(1) if match else ""

    def _replace_reference(self, match):
        group = match.group(1)
        reference_list = []
        if group.startswith("LIST:"):
            reference_list = self._parse_ref_list(group)
        else:
            # this case handles situation when chat return old :ref block
            # like: `:ref[CQS:ABC]` or `:ref[EXTERNAL:ABC]`
            reference_list.append(group)
        res = ""
        for reference in reference_list:
            doc_id = ""
            if reference.startswith("CQS:"):
                doc_id = self._extract_cqs_id(reference)
            elif reference.startswith("EXTERNAL:"):
                doc_id = self._extract_external_id(reference)
            for index, attribution in enumerate(self.sources):
                if attribution.id == doc_id:
                    # res += f'`:ref[{index}]`'
                    res += self.formatter.format(index, attribution)
        return res

    def parse_references(self, text: str) -> str:
        import re

        return re.sub(r"`:ref\[(.*?)\]`", self._replace_reference, text)


class CamelModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ChatInteractionTextResponseBlock(CamelModel):
    type: Literal["TEXT"]
    value: str


class ChatInteractionEngineResponseBlock(CamelModel):
    type: Literal["ENGINE"]
    answer: str


class ChatInteraction(CamelModel):

    input_message: str
    response_block: Union[
        ChatInteractionTextResponseBlock, ChatInteractionEngineResponseBlock
    ]
    interaction_timestamp: str
    date_created: datetime
    last_updated: datetime
    scope: Optional[str] = None
    audit_traces: list[dict] = Field(default=[])

    def to_chat_interaction(self, formatter: InlineAttributionFormatter):
        sources = parse_audit_traces(self.audit_traces)
        if self.response_block.type == "TEXT":
            answer = self._parse_references(
                self.response_block.value,
                sources,
                formatter,
            )
            return ChatInteractionModel(
                question=self.input_message,
                answer=answer,
                interaction_timestamp=self.interaction_timestamp,
                date_created=self.date_created,
                last_updated=self.last_updated,
                scope=self.scope,
                sources=sources,
            )
        elif self.response_block.type == "ENGINE":
            answer = self._parse_references(
                self.response_block.answer,
                sources,
                formatter,
            )
            return ChatInteractionModel(
                question=self.input_message,
                answer=answer,
                interaction_timestamp=self.interaction_timestamp,
                date_created=self.date_created,
                last_updated=self.last_updated,
                scope=self.scope,
                sources=sources,
            )
        else:
            raise BigdataClientError(
                f"Unknown response block type: {self.response_block.type}"
            )

    @staticmethod
    def _parse_references(
        text,
        chat_sources,
        formatter: InlineAttributionFormatter,
    ):
        parser = ReferenceParser(chat_sources, formatter)
        return parser.parse_references(text)


class ChatResponse(CamelModel):

    id: str
    name: str
    user_id: str
    date_created: datetime
    last_updated: datetime
    interactions: list[ChatInteraction]

    def to_chat_model(self, api_connection, formatter: InlineAttributionFormatter):
        return Chat(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            date_created=self.date_created,
            last_updated=self.last_updated,
            _interactions=[x.to_chat_interaction(formatter) for x in self.interactions],
            _api_connection=api_connection,
            _formatter=formatter,
            _loaded=True,
        )


class GetChatListResponseItem(CamelModel):

    id: str
    name: str
    user_id: str
    date_created: datetime
    last_updated: datetime

    def to_chat_model(self, api_connection, formatter: InlineAttributionFormatter):
        return Chat(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            date_created=self.date_created,
            last_updated=self.last_updated,
            _interactions=[],
            _api_connection=api_connection,
            _loaded=False,
            _formatter=formatter,
        )


class GetChatListResponse(CamelModel):
    root: list[GetChatListResponseItem]

    def to_chat_list(self, api_connection, formatter: InlineAttributionFormatter):
        return [x.to_chat_model(api_connection, formatter) for x in self.root]


class CreateNewChat(CamelModel):
    name: str = Field(min_length=1)


class ChatWSCompleteResponse(CamelModel):
    type: Literal["COMPLETE"]
    interaction_timestamp: str
    content_block: dict


class ChatWSAuditTraceResponse(CamelModel):
    type: Literal["AUDIT_TRACE"]
    trace: dict

    def to_chat_source(self) -> list[ChatSource]:
        return parse_audit_traces([self.trace])


class ChatWSNextResponse(CamelModel):
    type: Literal["NEXT"]
    content: str
    request_id: str
    sequence_number: int
    # message_delta_ms: int ## NOT USED FOR NOW


class ChatTracking(CamelModel):
    files: Optional[list[str]] = Field(default_factory=list)
    watchlists: Optional[list[str]] = Field(default_factory=list)
    prompt_task: Optional[str] = None
    prompt_topics: Optional[str] = None
    status: Optional[str] = None
    chat_start_location: Optional[str] = None
    follow_up_suggestion_index: Optional[str] = None
    platform: Literal["sdk"] = "sdk"
    platform_type: Optional[str] = None


class ChatAskRequest(CamelModel):
    request_id: str = ""  # Required, not used
    action: Literal["ChatWithMemoryRequest"] = "ChatWithMemoryRequest"
    chat_id: str
    input_message: str
    interaction_type: Literal["user_message"] = "user_message"
    scope: Optional[str] = None
    tracking: ChatTracking = ChatTracking()

"""SSE models"""

import json
from dataclasses import dataclass
from functools import partial

from aiohttp_sse_client.client import MessageEvent

from ..dtos import (
    AbsolidixCalculationsEventDTO,
    AbsolidixCollectionsEventDTO,
    AbsolidixDataSourcesEventDTO,
    AbsolidixErrorDTO,
    AbsolidixErrorEventDTO,
    AbsolidixEventDTO,
    AbsolidixPongEventDTO,
)
from ..helpers import absolidix_json_decoder


@dataclass(frozen=True)
class AbsolidixMessageEvent(MessageEvent):
    "SSE Message Event"

    type: str | None
    message: str
    data: str
    origin: str
    last_event_id: str

    @classmethod
    def from_dto(cls, data: MessageEvent) -> "AbsolidixMessageEvent":
        "Create model from DTO"
        return cls(
            type=data.type,
            message=data.message,
            data=data.data,
            origin=data.origin,
            last_event_id=data.last_event_id,
        )

    def to_dto(self) -> AbsolidixEventDTO:
        "Create DTO from model"
        try:
            if self.type is None and self.message == "" and self.data == "pong":
                return AbsolidixPongEventDTO(type="pong", data=None)
            for dto in (
                partial(AbsolidixErrorEventDTO, type="errors"),
                partial(AbsolidixDataSourcesEventDTO, type="datasources"),
                partial(AbsolidixCalculationsEventDTO, type="calculations"),
                partial(AbsolidixCollectionsEventDTO, type="collections"),
            ):
                if dto.keywords["type"] in [self.type, self.message]:
                    data = absolidix_json_decoder(self.data)

                    return dto(data=data)
        except json.JSONDecodeError as err:
            return AbsolidixErrorEventDTO(
                type="errors",
                data={
                    "req_id": "",
                    "data": [AbsolidixErrorDTO(status=400, error=str(err))],
                },
            )
        message = f"Unknown event type: {str(self)}"
        return AbsolidixErrorEventDTO(
            type="errors",
            data={"req_id": "", "data": [AbsolidixErrorDTO(status=400, error=message)]},
        )

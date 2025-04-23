# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "HashService",
    "EventService",
    "DAppService",
)

import typing

import attrs

from pletyvo.protocol import dapp
from pletyvo.codec.converter import uuidlike_converter
from pletyvo.codec.serializer import as_dict

if typing.TYPE_CHECKING:
    from . import abc
    from pletyvo.types import (
        QueryOption,
        JSONType,
        UUIDLike,
    )


class HashService(dapp.abc.HashService):
    def __init__(self, engine: abc.HTTPClient) -> None:
        self._engine = engine

    async def get_by_id(self, id: dapp.Hash) -> dapp.EventResponse:
        response: JSONType = await self._engine.get(f"/api/dapp/v1/hash/{id}")
        return dapp.EventResponse.from_dict(response)


class EventService(dapp.abc.EventService):
    def __init__(self, engine: abc.HTTPClient) -> None:
        self._engine = engine

    async def get(
        self, option: typing.Optional[QueryOption] = None
    ) -> list[dapp.Event]:
        response: JSONType = await self._engine.get(
            f"/api/dapp/v1/events{option or ''}"
        )
        return [dapp.Event.from_dict(d=event) for event in response]  # type: ignore

    async def get_by_id(self, id: UUIDLike) -> dapp.Event:
        id = uuidlike_converter(id)
        response: JSONType = await self._engine.get(f"/api/dapp/v1/events/{id}")
        return dapp.Event.from_dict(response)

    async def create(self, input: dapp.EventInput) -> dapp.EventResponse:
        response: JSONType = await self._engine.post(
            "/api/dapp/v1/events", body=as_dict(input)
        )
        return dapp.EventResponse.from_dict(response)


@attrs.define
class DAppService:
    hash: HashService = attrs.field()

    event: EventService = attrs.field()

    @classmethod
    def di(cls, engine: abc.HTTPClient) -> DAppService:
        hash = HashService(engine)
        event = EventService(engine)
        return cls(hash, event)

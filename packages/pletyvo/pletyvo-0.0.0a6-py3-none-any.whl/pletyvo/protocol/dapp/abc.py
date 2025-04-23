# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "Signer",
    "HashService",
    "EventService",
)

import typing
from abc import (
    ABC,
    abstractmethod,
)

if typing.TYPE_CHECKING:
    from .auth_header import AuthHeader
    from .hash import Hash
    from .event import (
        Event,
        EventInput,
        EventResponse,
    )
    from pletyvo.types import (
        UUIDLike,
        QueryOption,
    )


class Signer(ABC):
    @property
    @abstractmethod
    def sch(cls) -> int: ...

    @abstractmethod
    def sign(self, msg: bytes) -> bytes: ...

    @property
    @abstractmethod
    def pub(self) -> bytes: ...

    @property
    @abstractmethod
    def hash(self) -> Hash: ...

    @abstractmethod
    def auth(self, msg: bytes) -> AuthHeader: ...


class HashService(ABC):
    @abstractmethod
    async def get_by_id(self, id: Hash) -> EventResponse: ...


class EventService(ABC):
    @abstractmethod
    async def get(self, option: typing.Optional[QueryOption] = None) -> list[Event]: ...

    @abstractmethod
    async def get_by_id(self, id: UUIDLike) -> typing.Optional[Event]: ...

    @abstractmethod
    async def create(self, input: EventInput) -> EventResponse: ...

# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "ChannelService",
    "MessageService",
    "PostService",
)

import typing
from abc import (
    ABC,
    abstractmethod,
)

if typing.TYPE_CHECKING:
    from pletyvo.types import (
        QueryOption,
        UUIDLike,
    )
    from pletyvo.protocol import dapp, delivery
    from .channel import (
        Channel,
        ChannelCreateInput,
        ChannelUpdateInput,
    )
    from .post import (
        Post,
        PostCreateInput,
        PostUpdateInput,
    )
    from .message import (
        Message,
    )


class ChannelService(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUIDLike) -> Channel: ...

    @abstractmethod
    async def create(self, input: ChannelCreateInput) -> dapp.EventResponse: ...

    @abstractmethod
    async def update(self, input: ChannelUpdateInput) -> dapp.EventResponse: ...


class MessageService(ABC):
    @abstractmethod
    async def get(
        self, channel: UUIDLike, option: typing.Optional[QueryOption] = None
    ) -> list[Message]: ...

    @abstractmethod
    async def get_by_id(
        self, channel: UUIDLike, id: UUIDLike
    ) -> typing.Optional[Message]: ...

    @abstractmethod
    async def send(self, message: delivery.Message) -> None: ...


class PostService(ABC):
    @abstractmethod
    async def get(
        self, channel: UUIDLike, option: typing.Optional[QueryOption] = None
    ) -> list[Post]: ...

    @abstractmethod
    async def get_by_id(self, channel: UUIDLike, id: UUIDLike) -> Post: ...

    @abstractmethod
    async def create(self, input: PostCreateInput) -> dapp.EventResponse: ...

    @abstractmethod
    async def update(self, input: PostUpdateInput) -> dapp.EventResponse: ...

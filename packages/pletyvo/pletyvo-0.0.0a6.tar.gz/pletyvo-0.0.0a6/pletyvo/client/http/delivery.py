# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations
import contextlib

__all__: typing.Sequence[str] = (
    "ChannelService",
    "MessageService",
    "DeliveryService",
)

import typing

import attrs
from aiohttp.client_exceptions import ContentTypeError as AiohttpContentTypeError

from pletyvo.types import QueryOption
from pletyvo.codec.serializer import as_dict
from pletyvo.codec.converter import uuidlike_converter
from pletyvo.protocol import (
    dapp,
    delivery,
)

if typing.TYPE_CHECKING:
    from . import abc
    from pletyvo.types import (
        QueryOption,
        JSONType,
        UUIDLike,
    )


class ChannelService(delivery.abc.ChannelService):
    def __init__(
        self,
        engine: abc.HTTPClient,
        signer: dapp.abc.Signer,
        event: dapp.abc.EventService,
    ) -> None:
        self._engine = engine
        self._signer = signer
        self._event = event

    async def get_by_id(self, id: UUIDLike) -> delivery.Channel:
        id = uuidlike_converter(id)
        response: JSONType = await self._engine.get(f"/api/delivery/v1/channel/{id}")
        return delivery.Channel.from_dict(response)

    async def create(self, input: delivery.ChannelCreateInput) -> dapp.EventResponse:
        return await self._event.create(
            input=dapp.EventInput.signed(
                signer=self._signer,
                body=dapp.EventBody.create(
                    version=dapp.EventBodyType.BASIC,
                    data_type=dapp.DataType.JSON,
                    event_type=delivery.CHANNEL_CREATE_EVENT_TYPE,
                    value=as_dict(input),
                ),
            )
        )

    async def update(self, input: delivery.ChannelUpdateInput) -> dapp.EventResponse:
        return await self._event.create(
            input=dapp.EventInput.signed(
                signer=self._signer,
                body=dapp.EventBody.create(
                    version=dapp.EventBodyType.BASIC,
                    data_type=dapp.DataType.JSON,
                    event_type=delivery.CHANNEL_UPDATE_EVENT_TYPE,
                    value=as_dict(input),
                ),
            )
        )


class PostService(delivery.abc.PostService):
    def __init__(
        self,
        engine: abc.HTTPClient,
        signer: dapp.abc.Signer,
        event: dapp.abc.EventService,
    ) -> None:
        self._engine = engine
        self._signer = signer
        self._event = event

    async def get(
        self, channel: UUIDLike, option: typing.Optional[QueryOption] = None
    ) -> list[delivery.Post]:
        channel = uuidlike_converter(channel)
        channel = uuidlike_converter(channel)
        response: JSONType = await self._engine.get(
            f"/api/delivery/v1/channel/{channel}/posts{str(option or '')}"  # noqa: E501
        )
        return [delivery.Post.from_dict(post) for post in response]

    async def get_by_id(self, channel: UUIDLike, id: UUIDLike) -> delivery.Post:
        channel, id = uuidlike_converter(channel), uuidlike_converter(id)
        response: JSONType = await self._engine.get(
            f"/api/delivery/v1/channel/{channel}/posts/{id}"
        )
        return delivery.Post.from_dict(response)

    async def create(self, input: delivery.PostCreateInput) -> dapp.EventResponse:
        return await self._event.create(
            input=dapp.EventInput.signed(
                signer=self._signer,
                body=dapp.EventBody.create(
                    version=dapp.EventBodyType.BASIC,
                    data_type=dapp.DataType.JSON,
                    event_type=delivery.POST_CREATE_EVENT_TYPE,
                    value=as_dict(input),
                ),
            )
        )

    async def update(self, input: delivery.PostUpdateInput) -> dapp.EventResponse:
        return await self._event.create(
            input=dapp.EventInput.signed(
                signer=self._signer,
                body=dapp.EventBody.create(
                    version=dapp.EventBodyType.BASIC,
                    data_type=dapp.DataType.JSON,
                    event_type=delivery.POST_UPDATE_EVENT_TYPE,
                    value=as_dict(input),
                ),
            )
        )


class MessageService(delivery.abc.MessageService):
    def __init__(
        self,
        engine: abc.HTTPClient,
        signer: dapp.abc.Signer,
    ) -> None:
        self._engine = engine
        self._signer = signer

    async def get(
        self, channel: UUIDLike, option: typing.Optional[QueryOption] = None
    ) -> list[delivery.Message]:
        channel = uuidlike_converter(channel)
        response: JSONType = await self._engine.get(
            f"/api/delivery/v1/channel/{channel}/messages" + str(option or "")
        )
        return [delivery.Message.from_dict(message) for message in response]

    async def get_by_id(
        self, channel: UUIDLike, id: UUIDLike
    ) -> delivery.Message | None:
        channel = uuidlike_converter(channel)
        response: JSONType = await self._engine.get(
            f"/api/delivery/v1/channels/{channel}/messages/{uuidlike_converter(id)}"
        )
        return delivery.Message.from_dict(response)

    async def send(self, message: delivery.Message) -> None:
        with contextlib.suppress(AiohttpContentTypeError):
            await self._engine.post(
                "/api/delivery/v1/channel/send", body=as_dict(message)
            )


@attrs.define
class DeliveryService:
    channel: ChannelService = attrs.field()

    post: PostService = attrs.field()

    message: MessageService = attrs.field()

    @classmethod
    def di(
        cls,
        engine: abc.HTTPClient,
        signer: dapp.abc.Signer,
        event: dapp.abc.EventService,
    ):
        channel = ChannelService(engine, signer, event)
        post = PostService(engine, signer, event)
        message = MessageService(engine, signer)
        return cls(channel, post, message)

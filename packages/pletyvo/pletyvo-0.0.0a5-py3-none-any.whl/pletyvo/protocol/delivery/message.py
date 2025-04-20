# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "Message",
    "MessageInput",
)

import typing
from uuid import UUID

import attrs

from pletyvo.protocol import dapp
from pletyvo.codec.converter import (
    dapp_hash_converter,
    dapp_auth_header_converter,
    dapp_event_body_converter,
    uuidlike_converter,
)


message_content_validator = (
    attrs.validators.min_len(1),
    attrs.validators.max_len(2048),
)  # type: ignore[var-annotated]


@attrs.define(hash=True)
class Message:
    body: dapp.EventBody = attrs.field(converter=dapp_event_body_converter)

    auth: dapp.AuthHeader = attrs.field(converter=dapp_auth_header_converter)

    @classmethod
    def from_dict(cls, d: dict[str, typing.Any]) -> Message:
        return cls(
            body=d["body"],
            auth=d["auth"],
        )


@attrs.define
class MessageInput:
    id: UUID = attrs.field(converter=uuidlike_converter)

    channel: dapp.Hash = attrs.field(converter=dapp_hash_converter)

    content: str = attrs.field(validator=message_content_validator)

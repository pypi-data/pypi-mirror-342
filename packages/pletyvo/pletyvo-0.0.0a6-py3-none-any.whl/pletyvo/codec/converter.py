# Copyright (c) 2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "dapp_hash_converter",
    "dapp_auth_header_converter",
    "dapp_event_body_converter",
    "uuidlike_converter",
)

import typing
from uuid import UUID

from pletyvo.protocol import dapp

if typing.TYPE_CHECKING:
    from pletyvo.types import UUIDLike


def dapp_hash_converter(h: dapp.Hash | str) -> dapp.Hash:
    if isinstance(h, str):
        return dapp.Hash.from_str(h)
    return h


def dapp_auth_header_converter(
    d: dapp.AuthHeader | dict[str, typing.Any],
) -> dapp.AuthHeader:
    if isinstance(d, dict):
        return dapp.AuthHeader.from_dict(d)
    return d


def dapp_event_body_converter(
    b: dapp.EventBody | str | bytes | bytearray,
) -> dapp.EventBody:
    if isinstance(b, str):
        return dapp.EventBody.from_str(b)
    elif isinstance(b, bytes):
        return dapp.EventBody.from_bytes(b)
    elif isinstance(b, bytearray):
        return dapp.EventBody.from_bytearray(b)
    elif isinstance(b, memoryview):
        return dapp_event_body_converter(b.tobytes())
    return b


def uuidlike_converter(u: UUIDLike) -> UUID:
    return u if isinstance(u, UUID) else UUID(u)

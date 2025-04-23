# Copyright (c) 2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "padd",
    "uuid7",
)

import typing

import uuid
import uuid_utils


def padd(s: str) -> str:
    return s + "=" * (-len(s) % 4)


def uuid7(
    timestamp: typing.Optional[int] = None,
    nanos: typing.Optional[int] = None,
) -> uuid.UUID:
    return uuid.UUID(int=uuid_utils.uuid7(timestamp, nanos).int)

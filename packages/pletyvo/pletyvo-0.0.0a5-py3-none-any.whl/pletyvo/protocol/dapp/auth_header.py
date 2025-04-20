# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = ("AuthHeader",)

import typing
from base64 import b64decode

import attrs

from .hash import Hash


@attrs.define(hash=True)
class AuthHeader:
    sch: int = attrs.field()

    pub: bytes = attrs.field()

    sig: bytes = attrs.field()

    @property
    def author(self) -> Hash:
        return Hash.gen(self.sch, self.pub)

    @classmethod
    def from_dict(cls, d: dict[str, typing.Any]) -> AuthHeader:
        return cls(
            sch=d["sch"],
            pub=b64decode(d["pub"]),
            sig=b64decode(d["sig"]),
        )

# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "Schema",
    "ED25519",
)

import typing

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from . import abc
from .auth_header import AuthHeader
from .hash import Hash

if typing.TYPE_CHECKING:
    from os import PathLike


class Schema:
    ED25519 = 1


class ED25519(abc.Signer):
    def __init__(self, seed: bytes) -> None:
        self._private_key = Ed25519PrivateKey.from_private_bytes(seed)
        self._public_key = self._private_key.public_key()

    @classmethod
    def from_file(cls, path: str | PathLike[str]) -> ED25519:
        with open(path, "rb") as f:
            return cls(f.read())

    @classmethod
    def gen(cls) -> ED25519:
        return cls(Ed25519PrivateKey.generate().private_bytes_raw())

    @property
    def sch(cls) -> int:
        return Schema.ED25519

    def sign(self, msg: bytes) -> bytes:
        return self._private_key.sign(msg)

    @property
    def pub(self) -> bytes:
        return self._public_key.public_bytes_raw()

    @property
    def hash(self) -> Hash:
        return Hash.gen(
            sch=self.sch,
            data=self.pub,
        )

    def auth(self, msg: bytes) -> AuthHeader:
        return AuthHeader(
            sch=self.sch,
            pub=self.pub,
            sig=self.sign(msg),
        )

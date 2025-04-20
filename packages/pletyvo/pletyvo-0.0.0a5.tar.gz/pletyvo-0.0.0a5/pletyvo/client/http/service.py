# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = ("HTTPService",)

import typing

import attrs

from .dapp import DappService
from .delivery import DeliveryService

if typing.TYPE_CHECKING:
    from . import abc
    from pletyvo.protocol.dapp import abc as _dapp_abc


@attrs.define
class HTTPService:
    dapp: DappService = attrs.field()

    delivery: DeliveryService = attrs.field()

    @classmethod
    def _(cls, engine: abc.HTTPClient, signer: _dapp_abc.Signer) -> HTTPService:
        dapp = DappService._(engine)
        delivery = DeliveryService._(engine, signer, dapp.event)
        return cls(dapp, delivery)

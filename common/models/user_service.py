from dataclasses import dataclass
from .enums import Currency


@dataclass
class BalanceResponse:
    userId: int
    balance: float
    currency: Currency


@dataclass
class UpdateBalanceRequest:
    userId: int
    newBalance: float


@dataclass
class UpdateBalanceResponse:
    userId: int
    balance: float
    currency: Currency
from dataclasses import dataclass
from .enums import TransactionStatus


@dataclass
class PlaceBetRequest:
    userId: int
    betAmount: float


@dataclass
class PlaceBetResponse:
    userId: int
    transactionId: str
    status: TransactionStatus
    newBalance: float


@dataclass
class PayoutRequest:
    userId: int
    transactionId: str
    winAmount: float


@dataclass
class PayoutResponse:
    userId: int
    transactionId: str
    status: TransactionStatus
    newBalance: float
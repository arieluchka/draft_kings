from dataclasses import dataclass
from typing import List, Union
from .enums import GameOutcome, ReelSymbol


@dataclass
class SlotSpinRequest:
    userId: int
    betAmount: float
    transactionId: str


@dataclass
class SlotWinResult:
    userId: int
    outcome: GameOutcome
    winAmount: float
    reels: List[ReelSymbol]
    message: str


@dataclass
class SlotLoseResult:
    userId: int
    outcome: GameOutcome
    winAmount: float
    reels: List[ReelSymbol]
    message: str


@dataclass
class SlotSpinWinResponse:
    Win: SlotWinResult


@dataclass
class SlotSpinLoseResponse:
    Lose: SlotLoseResult


# Union type for either win or lose response
SlotSpinResponse = Union[SlotSpinWinResponse, SlotSpinLoseResponse]
from dataclasses import dataclass
from typing import List, Union
from .enums import GameOutcome, ReelSymbol


@dataclass
class SlotSpinRequest:
    userId: int
    betAmount: float
    transactionId: str


@dataclass
class SlotResult:
    userId: int
    outcome: GameOutcome
    winAmount: float
    reels: List[ReelSymbol]
    message: str

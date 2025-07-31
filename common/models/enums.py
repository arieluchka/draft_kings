from enum import Enum


class TransactionStatus(Enum):
    SUCCESS = "SUCCESS"
    # FAILED = "FAILED"
    # PENDING = "PENDING"


class GameOutcome(Enum):
    WIN = "WIN"
    LOSE = "LOSE"


class NotificationStatus(Enum):
    SENT = "SENT"
    # FAILED = "FAILED"
    # PENDING = "PENDING"


class Currency(Enum):
    USD = "USD"
    # EUR = "EUR"
    # GBP = "GBP"


class ReelSymbol(Enum):
    CHERRY = "Cherry"
    BELL = "Bell"
    # LEMON = "Lemon"
    # ORANGE = "Orange"
    # PLUM = "Plum"
    # BAR = "Bar"
    # SEVEN = "Seven"
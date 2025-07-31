from dataclasses import dataclass
from .enums import NotificationStatus


@dataclass
class NotificationRequest:
    userId: int
    transactionId: str
    message: str


@dataclass
class NotificationResponse:
    status: NotificationStatus
    notificationId: str
from common.hosts import NOTIFICATION_SERVICE
from common.models.notification_service import NotificationRequest, NotificationResponse
from common.api_models.base_client import BaseAPIClient


class NotificationServiceAPI(BaseAPIClient):
    """API client for Notification Service"""

    def __init__(self):
        super().__init__(NOTIFICATION_SERVICE)

    def send_notification(self, request: NotificationRequest) -> NotificationResponse:
        """Send a notification to user"""
        data = {
            "userId": request.userId,
            "transactionId": request.transactionId,
            "message": request.message
        }
        response = self.__post("/notify", data)
        return response.json()

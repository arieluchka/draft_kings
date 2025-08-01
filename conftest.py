import pytest
from common.api_models.game_service_api import GameServiceAPI
from common.api_models.user_service_api import UserServiceAPI
from common.api_models.notification_service_api import NotificationServiceAPI
from common.api_models.payment_service_api import PaymentServiceAPI


class CasinoAPI:
    def __init__(self):
        self.game_service = GameServiceAPI()
        self.user_service = UserServiceAPI()
        self.notification_service = NotificationServiceAPI()
        self.payment_service = PaymentServiceAPI()

@pytest.fixture(scope="session")
def casino_api():
    return CasinoAPI()

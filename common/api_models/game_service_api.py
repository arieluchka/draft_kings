from common.hosts import GAME_SERVICE
from common.models.game_service import SlotSpinRequest, SlotResult
from common.api_models.base_client import BaseAPIClient


class GameServiceAPI(BaseAPIClient):
    """API client for Game Service"""

    def __init__(self):
        super().__init__(GAME_SERVICE)

    def spin_slot(self, request: SlotSpinRequest) -> SlotResult:
        """Spin the slot machine"""
        data = {
            "userId": request.userId,
            "betAmount": request.betAmount,
            "transactionId": request.transactionId
        }
        response = self.__post("/slot/spin", data)
        return response.json()

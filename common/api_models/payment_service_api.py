from common.hosts import PAYMENYT_SERVICE
from common.models.payment_service import PlaceBetRequest, PlaceBetResponse, PayoutRequest, PayoutResponse
from common.api_models.base_client import BaseAPIClient

class PaymentServiceAPI(BaseAPIClient):
    """API client for Payment Service"""

    def __init__(self):
        super().__init__(PAYMENYT_SERVICE)

    def place_bet(self, request: PlaceBetRequest) -> PlaceBetResponse:
        """Place a bet and deduct from user balance"""
        data = {
            "userId": request.userId,
            "betAmount": request.betAmount
        }
        response = self.__post("/payment/placeBet", data)
        return response.json()

    def process_payout(self, request: PayoutRequest) -> PayoutResponse:
        """Process payout for winning bet"""
        data = {
            "userId": request.userId,
            "transactionId": request.transactionId,
            "winAmount": request.winAmount
        }
        response = self.__post("/payment/payout", data)
        return response.json()

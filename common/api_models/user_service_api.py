from common.hosts import USER_SERVICE
from common.models.user_service import BalanceResponse, UpdateBalanceRequest, UpdateBalanceResponse
from common.api_models.base_client import BaseAPIClient


class UserServiceAPI(BaseAPIClient):
    """API client for User Service"""

    def __init__(self):
        super().__init__(USER_SERVICE)

    def get_balance(self, user_id: int) -> BalanceResponse:
        """Get user balance"""
        response = self.__get(f"/user/balance?userId={user_id}")
        return response.json()

    def update_balance(self, request: UpdateBalanceRequest) -> UpdateBalanceResponse:
        """Update user balance"""
        data = {
            "userId": request.userId,
            "newBalance": request.newBalance
        }
        response = self.__post(f"/user/update-balance", data)
        return response.json()

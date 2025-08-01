import requests
from typing import Dict, Any, Optional


class BaseAPIClient:
    """Base class for API clients with common HTTP methods"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None,
                      params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status() # Raise an error for bad responses
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")

    def __get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._make_request("GET", endpoint, params=params)

    def __post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._make_request("POST", endpoint, data=data)

    def __put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._make_request("PUT", endpoint, data=data)

    def __delete(self, endpoint: str) -> requests.Response:
        return self._make_request("DELETE", endpoint)

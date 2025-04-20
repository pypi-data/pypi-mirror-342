import requests

class FloodWaiveClient:
    def __init__(self, api_url: str, token: str, timeout: int = 10):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def validate_token(self) -> bool:
        """Validates the token via /auth/me endpoint."""
        try:
            response = requests.get(f"{self.api_url}/auth/me", headers=self.headers, timeout=self.timeout)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"❌ Token validation failed: {e}")
            return False

    def _get(self, endpoint: str, params: dict = None):
        """Wrapper for GET requests."""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, payload: dict = None):
        """Wrapper for POST requests."""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, headers=self.headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

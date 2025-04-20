import requests

class DeepWaiveForecast:
    def __init__(self, api_url: str, token: str):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def validate_token(self) -> bool:
        """Checks if the API token is valid."""
        try:
            response = requests.get(f"{self.api_url}/auth/me", headers=self.headers)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Connection failed: {e}")
            return False

    def get_forecast(self, location_id: str, lead_time_hours: int = 24):
        """Request a forecast for a specific location."""
        endpoint = f"{self.api_url}/forecast"
        params = {
            "location_id": location_id,
            "lead_time": lead_time_hours
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Forecast request failed: {e}")
            return None

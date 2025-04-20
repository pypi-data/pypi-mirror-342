import requests

class DeepWaiveRiskAnalyzer:
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

    def analyze_risk(self, area_id: str, event_date: str):
        """Run a risk analysis for a given area and date."""
        endpoint = f"{self.api_url}/risk-analysis"
        payload = {
            "area_id": area_id,
            "event_date": event_date
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Risk analysis failed: {e}")
            return None

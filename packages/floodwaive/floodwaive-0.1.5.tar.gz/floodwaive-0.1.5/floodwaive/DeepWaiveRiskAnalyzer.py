from floodwaive.FloodWaiveClient import FloodWaiveClient

class DeepWaiveRiskAnalyzer(FloodWaiveClient):
    """
    Handles risk analysis communication with the FloodWaive API.
    """

    def analyze_risk(self, area_id: str, event_date: str):
        """
        Run a risk analysis for a given area and date.

        Args:
            area_id (str): ID of the area to analyze.
            event_date (str): Date of the event in YYYY-MM-DD format.

        Returns:
            dict: Risk analysis result as JSON.
        """
        payload = {
            "area_id": area_id,
            "event_date": event_date
        }
        return self._post("/risk-analysis", payload=payload)

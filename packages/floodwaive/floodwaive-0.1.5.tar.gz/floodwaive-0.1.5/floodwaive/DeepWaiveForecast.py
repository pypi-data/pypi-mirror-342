from floodwaive.FloodWaiveClient import FloodWaiveClient

class DeepWaiveForecast(FloodWaiveClient):
    """
    Handles forecast-related communication with the FloodWaive API.
    """

    def get_forecast(self, location_id: str, lead_time_hours: int = 24):
        """
        Request a forecast for a specific location and lead time.

        Args:
            location_id (str): ID of the location to forecast.
            lead_time_hours (int): Forecast lead time in hours.

        Returns:
            dict: Forecast result as JSON.
        """
        params = {
            "location_id": location_id,
            "lead_time": lead_time_hours
        }
        return self._get("/forecast", params=params)

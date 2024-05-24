import unittest
from get_weather_skill import GetWeatherSkill
from unittest.mock import patch, MagicMock
import config  # Import your config file

class TestGetWeatherSkill(unittest.TestCase):

    @patch('requests.get')
    def test_get_noaa_weather_success(self, mock_get):
        """Tests successful weather retrieval."""
        # Mock location response
        mock_location_response = MagicMock()
        mock_location_response.status_code = 200
        mock_location_response.json.return_value = {
            "properties": {
                "relativeLocation": {
                    "properties": {
                        "city": "Springfield",
                        "state": "MO"
                    }
                },
                "forecast": "https://test-forecast-url.com" 
            }
        }

        # Mock forecast response
        mock_forecast_response = MagicMock()
        mock_forecast_response.status_code = 200
        mock_forecast_response.json.return_value = {
            'properties': {
                'periods': [
                    {
                        'temperature': 75,
                        'windSpeed': '10 mph',
                        'shortForecast': 'Sunny',
                        'isDaytime': True
                    },
                    {
                        'temperature': 60,
                        'windSpeed': '5 mph',
                        'shortForecast': 'Partly Cloudy',
                        'isDaytime': False 
                    }
                ]
            }
        }

        # Set up mock requests.get behavior
        def mock_requests_get(url, headers=None):
            if url == f"https://api.weather.gov/points/{config.latitude},{config.longitude}":
                return mock_location_response
            elif url == "https://test-forecast-url.com": 
                return mock_forecast_response
            else:
                raise ValueError(f"Unexpected URL: {url}")

        mock_get.side_effect = mock_requests_get 

        # Create skill instance and get response
        skill = GetWeatherSkill(latitude=config.latitude, longitude=config.longitude)
        response = skill.process("weather")

        # Assertions
        self.assertIn("Currently, it's 75 degrees in Springfield, MO", response)
        self.assertIn("with a wind speed of 10 mph", response)
        self.assertIn("It's sunny.", response)
        self.assertIn("You can expect more of the same today with a high of 75 and a low of 60.", response)

    @patch('requests.get')
    def test_get_noaa_weather_location_failure(self, mock_get):
        """Tests when the location API call fails."""
        mock_response = MagicMock()
        mock_response.status_code = 404  # Simulate a Not Found error
        mock_get.return_value = mock_response

        skill = GetWeatherSkill(latitude=config.latitude, longitude=config.longitude)
        response = skill.process("weather")

        # Assert None is returned (or adjust based on error handling in your code)
        self.assertIsNone(response)  

    @patch('requests.get')
    def test_get_noaa_weather_forecast_failure(self, mock_get):
        """Tests when the forecast API call fails."""
        mock_location_response = MagicMock()
        mock_location_response.status_code = 200
        mock_location_response.json.return_value = {
            "properties": {
                "relativeLocation": {
                    "properties": {
                        "city": "Springfield",
                        "state": "MO"
                    }
                },
                "forecast": "https://test-forecast-url.com"
            }
        }

        mock_forecast_response = MagicMock()
        mock_forecast_response.status_code = 500  # Simulate a server error
        mock_get.side_effect = [mock_location_response, mock_forecast_response]

        skill = GetWeatherSkill(latitude=config.latitude, longitude=config.longitude)
        response = skill.process("weather")

        # Assert None is returned (or adjust based on error handling in your code)
        self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()

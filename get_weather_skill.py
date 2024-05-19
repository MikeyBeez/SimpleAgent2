import requests
import config  

class GetWeatherSkill: 
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def process(self, input_text): 
        """Fetches and formats weather data from NOAA."""
        return self.get_noaa_weather(self.latitude, self.longitude)  # Call as method

    def trigger(self, input_text):
        """Determines if the skill should be activated."""
        trigger_phrases = [
            "what's the weather", 
            "get the weather forecast", 
            "weather",
            # ... Add more trigger phrases as needed
        ]
        return any(phrase in input_text.lower() for phrase in trigger_phrases)

    def get_noaa_weather(self, latitude, longitude):
        """Fetches basic weather data from NOAA, 
           includes error handling and checks for dangerous weather, 
           and formats the output for an Alexa-like response.
        """

        base_url = "https://api.weather.gov/points/"
        complete_url = f"{base_url}{latitude},{longitude}"

        headers = {
            "Authorization": f"Bearer {config.noaa_weather_token}"
        }

        try:
            response = requests.get(complete_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                try:
                    # Get location information
                    city = data['properties']['relativeLocation']['properties']['city']
                    state = data['properties']['relativeLocation']['properties']['state']

                    # Get forecast URL
                    forecast_url = data['properties']['forecast']
                    forecast_response = requests.get(forecast_url, headers=headers)

                    if forecast_response.status_code == 200:
                        forecast_data = forecast_response.json()

                        # Extract current weather details
                        current_period = forecast_data['properties']['periods'][0]
                        current_temp = current_period['temperature']
                        current_wind_speed = current_period['windSpeed']
                        current_short_forecast = current_period['shortForecast'].lower()

                        # Extract today's high and low temperatures
                        high_temp = None
                        low_temp = None
                        for period in forecast_data['properties']['periods']:
                            if period['isDaytime']:
                                high_temp = period['temperature']
                            else:
                                low_temp = period['temperature']
                            if high_temp is not None and low_temp is not None:
                                break

                        # Construct the Alexa-like response
                        weather_summary = (
                            f"Currently, it's {current_temp} degrees in {city}, {state} "
                            f"with a wind speed of {current_wind_speed}. "
                            f"It's {current_short_forecast}. "
                        )
                        if high_temp is not None and low_temp is not None:
                            weather_summary += (
                                f"You can expect more of the same today with a high of "
                                f"{high_temp} and a low of {low_temp}."
                            )

                        return weather_summary  # Return the formatted summary

                    else:
                        print(f"Error fetching forecast data: Status Code {forecast_response.status_code}")
                except KeyError as e:
                    print(f"Error: Unable to find weather data in response. {e}")
            elif response.status_code == 404:
                print("Error 404: Resource not found. Verify coordinates and API endpoint.")
            else:
                print(f"Error: Status code {response.status_code}. Check API documentation.")

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")

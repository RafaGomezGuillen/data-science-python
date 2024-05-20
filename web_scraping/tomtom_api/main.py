"""
TomTom API Documentation
Radius = 50.000 meters is the maximum
Limit = 100 results are the maximum request you can get
Category = 7309 is electric vehicle station TomTom API categorie ID
"""

# Libraries
from dataclasses import dataclass, asdict
import pandas as pd
import requests
import os
import sys

# Load TomTom API key
from dotenv import load_dotenv


# Constants
CONTINENTS = {
    'AM': {'lat': (-60, 83), 'lon': (-170, -35)},
    'EU': {'lat': (36, 70), 'lon': (-25, 40)},
    'AF': {'lat': (-35, 37), 'lon': (-18, 60)},
    'AS': {'lat': (15, 55), 'lon': (60, 180)},
    'OC': {'lat': (-50, -10), 'lon': (110, 180)}
}

INPUT_FILE_NAME = 'input.txt'
CURRENT_DIRECTORY = os.path.dirname(__file__)
INPUT_FILE_PATH = os.path.join(CURRENT_DIRECTORY, INPUT_FILE_NAME)
load_dotenv(os.path.join(CURRENT_DIRECTORY, '.env'))

# Load API keys from environment variable
API_KEYS = os.environ.get('API_KEYS').split(',')
LIMIT = 100
RADIUS = 50000
CATEGORY = 7309


@dataclass
class ChargerStation:
    """holds electric charger station data"""

    id: str = None
    name: str = None
    latitude: float = None
    longitude: float = None
    continent: str = None
    country: str = None
    iso_code: str = None
    city: str = None
    post_code: str = None
    address: str = None

    def extract_continent_from_coordinates(self):
        """helper function to extract continent from latitude and longitude"""

        for continent, values in CONTINENTS.items():
            if values['lat'][0] <= self.latitude <= values['lat'][1] and values['lon'][0] <= self.longitude <= values['lon'][1]:
                self.continent = continent


@dataclass
class ElectricCharger:
    """holds electric charger data"""

    charger_station_id: str = None
    formal_name: str = None
    current_type: str = None
    amps: int = None
    voltage: int = None
    power_kw: int = None


def save_to_csv(charging_stations: list, electric_chargers: list):
    print('\n\nSaving data frames...')
    # Convert lists of dictionaries to DataFrames
    charging_stations_df = pd.DataFrame(charging_stations)
    electric_chargers_df = pd.DataFrame(electric_chargers)

    # Create the directories if they don't exist in the current directory
    charger_station_dir = os.path.join(CURRENT_DIRECTORY, 'charger_station')
    electric_charger_dir = os.path.join(CURRENT_DIRECTORY, 'electric_charger')
    os.makedirs(charger_station_dir, exist_ok=True)
    os.makedirs(electric_charger_dir, exist_ok=True)

    # Save DataFrames to CSV files in the respective directories
    charging_stations_df.to_csv(
        os.path.join(charger_station_dir, 'charger_stations.csv'), index=False)
    electric_chargers_df.to_csv(
        os.path.join(electric_charger_dir, 'electric_chargers.csv'), index=False)


def main():
    # Read coordinates from input.txt file
    if os.path.exists(INPUT_FILE_PATH):
        with open(INPUT_FILE_PATH, 'r') as file:
            coordinates_list = file.readlines()
    else:
        print('Error: input.txt file not found.')
        sys.exit()

    # Creating lists
    charging_stations = []
    electric_chargers = []
    api_key_index = 0  # Start with the first API key

    for coordinates_str in coordinates_list:
        # Split the coordinates string by ','
        coordinates = coordinates_str.strip().split(',')
        if len(coordinates) != 2:
            print(
                f'Error: Invalid format for coordinates: {coordinates_str}')
            continue

        latitude, longitude = coordinates

        while api_key_index < len(API_KEYS):
            url_search_nearby = F'https://api.tomtom.com/search/2/nearbySearch/.json?ofs=0&lat={latitude}&lon={longitude}&limit={LIMIT}&radius={RADIUS}&categorySet={CATEGORY}&relatedPois=off&key={API_KEYS[api_key_index]}'

            try:
                response = requests.get(url_search_nearby)
                if response.status_code == 403:
                    api_key_index += 1  # Use the next API key
                    print(
                        f'\nChanging API KEY to:\n\n{API_KEYS[api_key_index]}\n-----------------------')
                    continue  # Retry with the next API key
                elif response.status_code == 200:
                    print(f'\n\nDoing request to: {url_search_nearby}')
                    response.raise_for_status()  # Throw an exception if the request is unsuccessful

                    data = response.json()['results']

                    for station in data:
                        charger = ChargerStation()

                        try:
                            charger.id = station.get('id', '')
                            charger.name = station['poi'].get('name', '')
                            charger.latitude = station['position'].get(
                                'lat', 0)
                            charger.longitude = station['position'].get(
                                'lon', 0)
                            charger.country = station['address'].get(
                                'country', '')
                            charger.iso_code = station['address'].get(
                                'countryCode', '')
                            charger.city = station['address'].get(
                                'localName', '')
                            charger.post_code = station['address'].get(
                                'postalCode', '')
                            charger.address = station['address'].get(
                                'freeformAddress', '')
                        except KeyError as e:
                            print(f'KeyError: {e} not found in the dictionary')

                        charger.extract_continent_from_coordinates()
                        charging_stations.append(asdict(charger))

                        # Check if 'chargingPark' key exists before accessing 'chargingPark'
                        if 'chargingPark' in station and 'connectors' in station['chargingPark']:
                            connectors = station['chargingPark']['connectors']
                            
                            for connector in connectors:
                                electric_charger = ElectricCharger(
                                    charger_station_id=station.get('id', ''),
                                    formal_name=connector.get(
                                        'connectorType', ''),
                                    current_type=connector.get(
                                        'currentType', ''),
                                    amps=connector.get('currentA', 0),
                                    voltage=connector.get('voltageV', 0),
                                    power_kw=connector.get('ratedPowerKW', 0),
                                )

                                electric_chargers.append(asdict(electric_charger))
                break  # Exit the while loop if the request was successful
            except requests.exceptions.RequestException as e:
                print(f'RequestException: {e}')
            except KeyError as e:
                print(f'Error making API request RequestException: {e}')

    save_to_csv(charging_stations, electric_chargers)


if __name__ == '__main__':
    main()

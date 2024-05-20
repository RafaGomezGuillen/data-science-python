import pandas as pd
import argparse
import os
import sys

from playwright.sync_api import sync_playwright
from geopy.geocoders import Nominatim
from dataclasses import dataclass, asdict

# Constants
INPUT_FILE_NAME = 'input.txt'
INPUT_FILE_PATH = os.path.join(os.getcwd(), INPUT_FILE_NAME)

# Charger stations fields
NAME_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'
ADDRESS_XPATH = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
WEBSITE_XPATH = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
PHONE_NUMBER_XPATH = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'

# Electric chargers fields classes
FORMAL_NAME_CLASS = '.JpCtJf'
POWER_KW_CLASS = '.NiVgee.WAmrC'
QUANTITY_CLASS = '.lmLZWe'

@dataclass
class ChargerStation:
    """holds charger station data"""

    id: int = None
    name: str = None
    address: str = None
    latitude: float = None
    longitude: float = None
    city: str = None
    post_code: str = None
    country: str = None
    continent: str = None
    iso_code: str = None

    def extract_city_post_iso_code_country(self):
        """Extract city, postcode, ISO Code and country from the address string."""
        geolocator = Nominatim(user_agent='google_maps_api')
        location = geolocator.geocode(self.address)
        address_parts = [part.strip() for part in location.address.split(',')]

        self.city = address_parts[-3]  # Extract city
        self.post_code = address_parts[-2]  # Extract postcode
        self.country = address_parts[-1]  # Extract country

        location = geolocator.reverse(
            [self.latitude, self.longitude], exactly_one=True)
        address = location.raw['address']
        self.iso_code = address.get(
            'country_code', '').upper()  # Extract ISO code


@dataclass
class ElectricCharger:
    """holds electric charger data"""

    charger_station_id: int = None
    formal_name: str = None
    power_kw: str = None
    quantity: str = None


def extract_coordinates_from_url(url: str) -> tuple[float, float]:
    """helper function to extract coordinates from url"""

    coordinates = url.split('/@')[-1].split('/')[0]
    # return latitude, longitude
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])


def extract_continent_from_coordinates(latitude: float, longitude: float) -> str:
    """helper function to extract continent from latitude and longitude"""

    # Define the continents with their approximate latitude and longitude ranges
    continents = {
        'AM': {'lat': (-60, 83), 'lon': (-170, -35)},
        'EU': {'lat': (36, 70), 'lon': (-25, 40)},
        'AF': {'lat': (-35, 37), 'lon': (-18, 60)},
        'AS': {'lat': (15, 55), 'lon': (60, 180)},
        'OC': {'lat': (-50, -10), 'lon': (110, 180)}
    }

    # Check each continent to see if the coordinates fall within their range
    for continent, values in continents.items():
        if values['lat'][0] <= latitude <= values['lat'][1] and values['lon'][0] <= longitude <= values['lon'][1]:
            return continent

    return 'Unknown continent'


def main():

    ########
    # input
    ########

    # read search from arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--total', type=int)
    args = parser.parse_args()

    if args.total:
        total = args.total
    else:
        # if no total is passed, we set the value to a large number
        total = 1_000_000

    # Read coordinates from input.txt file
    if os.path.exists(INPUT_FILE_PATH):
        with open(INPUT_FILE_PATH, 'r') as file:
            coordinates_list = file.readlines()
    else:
        print('Error: input.txt file not found.')
        sys.exit()

    ###########
    # scraping
    ###########

    all_charger_list = []
    all_electric_charger_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.google.com/maps')
        
        # Initialize charger station ID
        charger_station_id = 1  

        for coordinates_str in coordinates_list:
            # Split the coordinates string by ','
            coordinates = coordinates_str.strip().split(',')
            if len(coordinates) != 2:
                print(
                    f'Error: Invalid format for coordinates: {coordinates_str}')
                continue

            latitude, longitude = coordinates

            # Construct the coordinates string
            coordinates_str = f'{latitude},{longitude}'

            for search_for in ['EV Chargers']:
                print(f'-----\n{search_for} in {coordinates_str}'.strip())

                # Pressing latitude and longitude
                page.locator(
                    '//input[@id="searchboxinput"]').fill(coordinates_str)
                page.keyboard.press('Enter')
                page.wait_for_timeout(3000)

                # Pressing Query 'EV Chargers'
                page.locator('//input[@id="searchboxinput"]').fill(search_for)

                page.keyboard.press('Enter')
                page.wait_for_timeout(3000)

                # scrolling
                page.hover(
                    '//a[contains(@href, "https://www.google.com/maps/place")]')

                # this variable is used to detect if the bot
                # scraped the same number of listings in the previous iteration
                previously_counted = 0
                while True:
                    page.mouse.wheel(0, 10000)
                    page.wait_for_timeout(3000)

                    if (
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        >= total
                    ):
                        listings = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).all()[:total]
                        listings = [listing.locator('xpath=..')
                                    for listing in listings]
                        print(f'Total Scraped: {len(listings)}')
                        break
                    else:
                        # logic to break from loop to not run infinitely
                        # in case arrived at all available listings
                        if (
                            page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count()
                            == previously_counted
                        ):
                            listings = page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).all()
                            print(
                                f'Arrived at all available\nTotal Scraped: {len(listings)}')
                            break
                        else:
                            previously_counted = page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count()
                            print(
                                f'Currently Scraped: ',
                                page.locator(
                                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                                ).count(),
                            )

                # scraping
                charger_list = []
                electric_charger_list = []

                for listing in listings:
                    try:
                        listing.click()
                        page.wait_for_timeout(2500)

                        charger_station = ChargerStation()
                        charger_station.id = charger_station_id

                        if page.locator(NAME_XPATH).count() > 0:
                            charger_station.name = page.locator(NAME_XPATH).all()[
                                0].inner_text()
                        else:
                            charger_station.name = ''
                        if page.locator(ADDRESS_XPATH).count() > 0:
                            charger_station.address = page.locator(ADDRESS_XPATH).all()[
                                0].inner_text()
                        else:
                            charger_station.address = ''

                        # Extract coordinates (latitude and longitude)
                        charger_station.latitude, charger_station.longitude = extract_coordinates_from_url(
                            page.url)

                        # Extract continent
                        charger_station.continent = extract_continent_from_coordinates(
                            charger_station.latitude, charger_station.longitude)

                        # Extract city, post code, ISO code and country
                        charger_station.extract_city_post_iso_code_country()

                        # Locate and count the number of electric chargers per charger station
                        electric_charger_div_container = listing.locator(
                            '.m6QErb')
                        electric_charger_count = electric_charger_div_container.locator(
                            '.MngOvd').count()

                        # Loop through each electric charger
                        for i in range(1, electric_charger_count + 1):
                            # Construct the index
                            index = i + 1

                            # Construct ElectricCharger object
                            electric_charger = ElectricCharger()
                            electric_charger.charger_station_id = charger_station_id

                            # Find the corresponding elements using class names
                            formal_name_elements = page.locator(
                                f'div.MngOvd:nth-child({index}) {FORMAL_NAME_CLASS}').all()
                            power_kw_elements = page.locator(
                                f'div.MngOvd:nth-child({index}) {POWER_KW_CLASS}').all()
                            quantity_elements = page.locator(
                                f'div.MngOvd:nth-child({index}) {QUANTITY_CLASS}').all()

                            # Check if all elements are found
                            if formal_name_elements and power_kw_elements and quantity_elements:
                                # Extract text content from the elements
                                electric_charger.formal_name = formal_name_elements[0].inner_text(
                                )
                                electric_charger.power_kw = power_kw_elements[0].inner_text(
                                )
                                electric_charger.quantity = quantity_elements[0].inner_text(
                                )

                                # Add electric charger to the list
                                electric_charger_list.append(asdict(electric_charger))
                            else:
                                print(
                                    f'Error: Electric charger details not found for index {index}')

                        charger_list.append(asdict(charger_station))
                        charger_station_id += 1  # Increment charger_station_id
                    except Exception as e:
                        print(f'Error occurred: {e}')

                # Add the lists of chargers and electric chargers to the main lists
                all_charger_list.extend(charger_list)
                all_electric_charger_list.extend(electric_charger_list)

        # Convert lists to pandas DataFrames
        charger_stations_df = pd.DataFrame(all_charger_list)
        electric_chargers_df = pd.DataFrame(all_electric_charger_list)

        # Save DataFrames to CSV files
        charger_stations_df.to_csv('all_charger_stations.csv', index=False)
        electric_chargers_df.to_csv('all_electric_chargers.csv', index=False)

        browser.close()


if __name__ == '__main__':
    main()

"""This script serves as an example on how to use Python 
   & Playwright to scrape/extract data from Google Maps"""

from playwright.sync_api import sync_playwright
from geopy.geocoders import Nominatim
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os


# Business fields
NAME_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'
ADDRESS_XPATH = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
WEBSITE_XPATH = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
PHONE_NUMBER_XPATH = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'


@dataclass
class Business:
    """holds Business data"""

    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
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
class BusinessList:
    """holds list of Business objects,
    and save to csv file
    """

    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep='_'
        )

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f'output/{filename}.csv', index=False)


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
    parser.add_argument('-s', '--search', type=str)
    parser.add_argument('-t', '--total', type=int)
    parser.add_argument('-c', '--city', type=str)
    args = parser.parse_args()

    if args.search:
        search_list = [args.search]

    if args.total:
        total = args.total
    else:
        # if no total is passed, we set the value to random big number
        total = 1_000_000

    ###########
    # scraping
    ###########
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto('https://www.google.com/maps', timeout=60000)
        for search_for_index, search_for in enumerate(search_list):
            print(
                f'-----\n{search_for_index} - {search_for} in {args.city}'.strip())

            # Pressing City
            page.locator('//input[@id="searchboxinput"]').fill(args.city)
            page.wait_for_timeout(3000)

            page.keyboard.press('Enter')
            page.wait_for_timeout(5000)

            # Pressing Query
            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(3000)

            page.keyboard.press('Enter')
            page.wait_for_timeout(5000)

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
                    listings = [listing.locator("xpath=..")
                                for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
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
                            f"Arrived at all available\nTotal Scraped: {len(listings)}")
                        break
                    else:
                        previously_counted = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        print(
                            f"Currently Scraped: ",
                            page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count(),
                        )

            business_list = BusinessList()

            # scraping
            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(2500)

                    business = Business()

                    if page.locator(NAME_XPATH).count() > 0:
                        business.name = page.locator(NAME_XPATH).all()[
                            0].inner_text()
                    else:
                        business.name = ''
                    if page.locator(ADDRESS_XPATH).count() > 0:
                        business.address = page.locator(ADDRESS_XPATH).all()[
                            0].inner_text()
                    else:
                        business.address = ''
                    if page.locator(WEBSITE_XPATH).count() > 0:
                        business.website = page.locator(WEBSITE_XPATH).all()[
                            0].inner_text()
                    else:
                        business.website = ''
                    if page.locator(PHONE_NUMBER_XPATH).count() > 0:
                        business.phone_number = page.locator(
                            PHONE_NUMBER_XPATH).all()[0].inner_text()
                    else:
                        business.phone_number = ''

                    business.latitude, business.longitude = extract_coordinates_from_url(
                        page.url)

                    business.continent = extract_continent_from_coordinates(
                        business.latitude, business.longitude)
                    business.extract_city_post_iso_code_country()

                    business_list.business_list.append(business)
                except Exception as e:
                    print(f'Error occured: {e}')

            #########
            # output
            #########
            business_list.save_to_csv(
                f'google_maps_data_{args.city}_{search_for}'.replace(' ', '_'))

        browser.close()


if __name__ == '__main__':
    main()

# TomTom API Data Retrieval

This Python script fetches data from the TomTom API for electric vehicle charging stations based on provided coordinates. It extracts information about charging stations and their electric chargers, saving the results into CSV files.

## Requirements

- Python 3.x
- requests
- pandas
- dotenv

## Configuration

**API Key**: You need to obtain a TomTom API key and store it in a `.env` file as **TOMTOM_API_KEY**.

**Input File**: Provide coordinates in a text file named `input.txt`, each line containing latitude and longitude separated by a comma.

### input.txt file example

Each line represents a city (latitude,longitude).

```txt
54.687157,25.279652
54.898521,23.903597
55.7172,21.1175
55.93333,23.31667
```

## Usage

Run the script `main.py`. It reads coordinates from `input.txt` and queries the TomTom API for charging stations near those coordinates.

## Constants

- **Radius**: Maximum search radius (default: 50,000 meters).
- **Limit**: Maximum number of results per request (default: 100).
- **Category**: TomTom API category ID for electric vehicle stations (default: 7309).
- **Offset**: Pagination offset for requests (default: 0).

## Data Classes

### ChargerStation

- **id**: Station ID
- **name**: Station name
- **latitude**: Latitude
- **longitude**: Longitude
- **continent**: Continent (derived from coordinates)
- **country**: Country
- **iso_code**: ISO country code
- **city**: City
- **post_code**: Postal code
- **address**: Full address

### ElectricCharger

- **charger_station_id**: ID of associated charger station
- **formal_name**: Charger type/formal name
- **current_type**: Electric current type
- **amps**: Ampere rating
- **voltage**: Voltage rating
- **power_kw**: Power rating in kilowatts
- **quantity**: Number of chargers available

## Functions

### save_to_csv(charging_stations, electric_chargers)

Saves charging station and electric charger data to CSV files in respective directories.

### main()

- Reads coordinates from input.txt.
- Queries the TomTom API for charging stations near the provided coordinates.
- Processes the API response, extracts data, and saves it to CSV files.

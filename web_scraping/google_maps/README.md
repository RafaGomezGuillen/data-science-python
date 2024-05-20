# Google Maps Web Scraping

## Running `main.py`

The `main.py` file is used to search for EV chargers at specific coordinates (latitude, longitude).

```cmd
python main.py -t=<how many EV chargers>
```

### Setting up the `input.txt` File

The coordinates need to be set in the `input.txt` file in the same directory as `main.py`. Each line represents a city:

```txt
52.229675,21.012230
50.064651,19.944981
52.406376,16.925167
54.3609751,18.5252211
51.2179933,22.3989632
```

### Example

```cmd
python main.py -t=10
```

### Output

> [!WARNING]
> The files will overwrite so do a copy if you already have an output.

- All EV chargers will be stored in a file called `all_charger_stations.csv`
- All electric chargers will be stored in a file called `all_electric_chargers.csv`

Code based on [google_maps_scraper repository by Amin Boutarfi](https://github.com/amineboutarfi/google_maps_scraper/tree/master)

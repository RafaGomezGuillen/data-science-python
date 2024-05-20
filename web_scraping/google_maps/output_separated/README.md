# Google Maps Web Scraping (Output Separated)

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

The EV Chargers and their electric chargers will be seperated in different CSV files.

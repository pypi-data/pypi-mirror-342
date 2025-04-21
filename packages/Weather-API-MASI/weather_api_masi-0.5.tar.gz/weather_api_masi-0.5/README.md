# Weather_API_MASI

Weather_API_MASI is a Python library for retrieving hourly weather and AQI (Air Quality Index) data.

Output/data is given in csv files.

This is a beta version of the Python API for Scraping Weather and Air Quality Data by Location and Date.
Please contact masilab@list.vanderbilt.edu for any questions.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Weather_API_MASI.

```bash
pip install Weather-API-MASI
```

## Usage

```python
from Weather_API_MASI import Weather

'''
There are two required parameters (city name and a start date in YYYY-MM-DD format).
The optional parameters are the end date, a boolean value representing if you'd like a visualization of data availability, and cache configurations.

Before creating any objects, a .env file with NOAA's API (AIRNOW_API_KEY="") and Nominatim's user agent must be created in the root directory (NOMINATIM_USER_AGENT="").

cache_config, if provided, must be in a dictionary format with keys being "cache_dir", "max_age_days", "max_cache_size_gb", and "compression".
Here is an example:
cache_config = {
    "cache_dir": r"C:\Users\Jane Doe\Desktop\weatherCache",
    "max_age_days": 0.01,
    "max_cache_size_gb": 10,
    "compression": "bz2"
}
'''
obj1 = Weather("2025-02-20", "nashville")
obj2 = Weather("2023-11-23", "los angeles", "2023-12-23")
obj3 = Weather("2023-01-02", "philadelphia", "2024-02-18", True)
obj4 = Weather("2023-01-02", "philadelphia", "2024-02-18", True, cache_config)


# These methods can be called on any obj
obj1.generate_hourly_data()  # A CSV file containing hourly data for the start date will be created.
obj1.generate_yearly_hourly_data() # "A CSV file containing hourly data for the start date's year will be created.
obj1.generate_AQI_data() # A CSV file containing AQI data for the start date will be created.
obj1.get_data_availability() # A visualization of data availability will be created as a data_avail.png

# This method can be called if an end date is provided
obj2.generate_hourly_data_range() # A CSV file containing hourly data between the start and end dates will be created.

# This is a static method, so it can be run on the Weather class
Weather.clear_cache(cache_config["cache_dir"]) # All cached data in provided cache location will be cleared.
Weather.clear_cache() # All cached data in the default location (~/.weather_cache) will be cleared
```

## CLI Command

You can use command line interface (CLI) for this package.
**Weather-API-MASI {city} {start date} --endDate {end date} --v {boolean} --cache-dir {file location} --max-cache-age {number of days} --max-cache-size {number of gigabytes}**
end date is optional.

This CLI command will provide AQI data as well as hourly data on a single day and an entire year.
Depending on the third optional parameter, hourly data in a time range will also be provided.
cd
```bash
Weather-API-MASI nashville 2025-02-20
```
```bash
Weather-API-MASI "los angeles" 2023-11-23 --endDate 2023-12-23 --v True
```
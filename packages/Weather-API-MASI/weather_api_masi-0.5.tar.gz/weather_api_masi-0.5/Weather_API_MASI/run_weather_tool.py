import sys
import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from geopy.geocoders import Nominatim
import argparse
import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import shutil
from datetime import datetime
import json
from pathlib import Path
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class WeatherAPIValidator:
    @staticmethod
    def validate_airnow_api(api_key: str) -> bool:
        """Validate AirNow API key"""
        test_url = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude=40.7128&longitude=-74.0060&distance=25&API_KEY={api_key}"
        try:
            response = requests.get(test_url)
            return response.status_code == 200
        except:
            return False

    @staticmethod
    def validate_nominatim(user_agent: str) -> bool:
        """Validate Nominatim user agent by making a test request"""
        try:
            geolocator = Nominatim(user_agent=user_agent)
            location = geolocator.geocode("New York")
            return location is not None
        except:
            return False

class WeatherCache:
    """Manages weather data caching operations"""
    
    def __init__(self, cache_config: Optional[Dict[str, Any]] = None):
        # Default configuration
        self.config = {
            'cache_dir': os.path.expanduser('~/.weather_cache'), # home directory
            'max_age_days': 30, # cache will be refreshed after 30 days
            'max_cache_size_gb': 10,  # max cache size in GB
            'compression': 'gzip'  # Compress cached files to save space
        }
        
        # Update with user configuration if provided
        if cache_config:
            self.config.update(cache_config)
            
        # Create cache directory if it doesn't exist
        os.makedirs(self.config['cache_dir'], exist_ok=True)
        self._init_cache_index()
        
        # Setup logging
        logging.basicConfig(
            filename=os.path.join(self.config['cache_dir'], 'cache.log'),
            level=logging.INFO
        )

    def _init_cache_index(self):
        """Initialize or load cache index"""
        self.index_path = os.path.join(self.config['cache_dir'], 'cache_index.json')
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r') as f:
                self.cache_index = json.load(f)
        else:
            self.cache_index = {}
        self._cleanup_old_entries()

    def _cleanup_old_entries(self):
        """Remove expired entries and manage cache size"""
        current_time = datetime.now()
        updated_index = {}
        total_size = 0

        # Sort entries by last access time
        sorted_entries = sorted(
            self.cache_index.items(),
            key=lambda x: x[1]['last_accessed'],
            reverse=True
        )

        for key, metadata in sorted_entries:
            file_path = os.path.join(self.config['cache_dir'], metadata['filename'])
            
            # Skip if file doesn't exist
            if not os.path.exists(file_path):
                continue

            file_age_days = (current_time - datetime.fromisoformat(metadata['last_accessed'])).days
            file_size = os.path.getsize(file_path) / (1024 * 1024 * 1024)  # Size in GB
            
            # Keep file if it's within age limit and size limit
            if (file_age_days <= self.config['max_age_days'] and 
                total_size + file_size <= self.config['max_cache_size_gb']):
                updated_index[key] = metadata
                total_size += file_size
            else:
                try:
                    os.remove(file_path)
                    logging.info(f"Removed expired cache file: {file_path}")
                except OSError as e:
                    logging.error(f"Error removing cache file: {e}")

        self.cache_index = updated_index
        self._save_index()

    def _save_index(self):
        """Save cache index to disk"""
        with open(self.index_path, 'w') as f:
            json.dump(self.cache_index, f)

class Weather:
    def __init__(self, date: str, city: str, endDate: Optional[str] = None, v=False, 
                 cache_config: Optional[Dict[str, Any]] = None):
        """
        Initialize Weather class with required API credentials from .env file
        """
        # Load environment variables
        if not load_dotenv():
            raise EnvironmentError("No .env file found. Please create one with AIRNOW_API_KEY and NOMINATIM_USER_AGENT")

        # Get API credentials
        self.airnow_api_key = os.getenv('AIRNOW_API_KEY')
        self.nominatim_user_agent = os.getenv('NOMINATIM_USER_AGENT')

        # Validate API credentials
        if not self.airnow_api_key:
            raise ValueError("AIRNOW_API_KEY not found in .env file")
        if not self.nominatim_user_agent:
            raise ValueError("NOMINATIM_USER_AGENT not found in .env file")

        # Validate API key and user agent
        validator = WeatherAPIValidator()
        if not validator.validate_airnow_api(self.airnow_api_key):
            raise ValueError("Invalid AirNow API key")
        if not validator.validate_nominatim(self.nominatim_user_agent):
            raise ValueError("Invalid Nominatim user agent or connection error")

        # Initialize browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver = driver
        
        # Set instance variables
        self.v = v
        self.date = date
        self.city = city
        self.end_date = endDate 
        self.yearly_df = pd.DataFrame()
        
        # Initialize cache manager
        self.cache_manager = WeatherCache(cache_config)
        
    def _get_cache_key(self, data_type: str) -> str:
        """Generate unique cache key"""
        start_year = int(self.date.split('-')[0])
        end_year = int(self.end_date.split('-')[0])

        years = [f"{self.city.lower()}_{year}_{data_type}" for year in range(start_year, end_year + 1)]
        return years

    def _get_from_cache(self, data_type: str) -> Optional[pd.DataFrame]:
        """Retrieve DataFrame from pickle cache if available"""
        cache_key = self._get_cache_key(data_type)
        for key in cache_key:
            if key in self.cache_manager.cache_index:
                metadata = self.cache_manager.cache_index[key]
                file_path = os.path.join(self.cache_manager.config['cache_dir'], metadata['filename'])

                if os.path.exists(file_path):
                    metadata['last_accessed'] = datetime.now().isoformat()
                    self.cache_manager._save_index()
                    compression = self.cache_manager.config.get("compression", "gzip")
                    return pd.read_pickle(file_path, compression=compression)
        return None

    def _save_to_cache(self, df: pd.DataFrame, data_type: str):
        """Save DataFrame to cache as a compressed pickle"""
        if df.empty:
            return

        cache_key = self._get_cache_key(data_type)
        for key in cache_key:
            filename = f"{key}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl.gz"
            file_path = os.path.join(self.cache_manager.config['cache_dir'], filename)
            compression = self.cache_manager.config.get("compression", "gzip")
            df.to_pickle(file_path, compression=compression)

            self.cache_manager.cache_index[key] = {
                'filename': filename,
                'created': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat(),
                'size_bytes': os.path.getsize(file_path)
            }
            self.cache_manager._save_index()

    def __get_yearly_content(self, links_set):
        """Fetch and combine all CSVs into a single pandas DataFrame"""
        # Try to get from cache first
        cached_data = self._get_from_cache("yearly")
        if cached_data is not None:
            logging.info(f"Cache hit for yearly data: {self.city} {self.date.split('-')[0]}")
            self.yearly_df = cached_data
            self.yearly_df.to_csv('yearlyData.csv', index=False)
            return

        # If not in cache, fetch and save
        if links_set:
            dfs = self.__fetch_all_data(links_set)
            if dfs:
                self.yearly_df = pd.concat(dfs, ignore_index=True)
                self.yearly_df.to_csv('yearlyData.csv', index=False)
                self._save_to_cache(self.yearly_df, "yearly")
            else:
                self.yearly_df = pd.DataFrame()
        else:
            print("Please try again.")

    def __get_daily_content(self, links_set):
        """Extract daily content into a pandas DataFrame"""
        # Try to get from cache first
        cached_data = self._get_from_cache("yearly")
        if cached_data is not None:
            print("getting cached")
            daily_data = cached_data[cached_data['DATE'].str.contains(self.date)]
            if self.v:
                print("getting data availability")
                self.__get_data_availability(daily_data)
            if not daily_data.empty:
                daily_data.to_csv('df_daily.csv', index=False)
                return daily_data

        try:
            total_rows = len(links_set)
            seen = False
            rows = []

            # Read the yearly content into a pandas DataFrame
            # yearly_df = pd.read_csv('yearlyContent.csv')

            # Iterate through the rows and filter by the date
            for _, row in self.yearly_df.iterrows():
                if self.date in row["DATE"]:
                    rows.append(row)
                    seen = True
                elif seen:  # If we've seen the date and now we haven't, stop iterating
                    total_rows -= 1
                    if total_rows <= 0:
                        break
                    seen = False

            # Convert filtered rows into a pandas DataFrame
            if rows:
                daily_df = pd.DataFrame(rows)
                print("Daily data extracted into DataFrame.")
                daily_df.to_csv('df_daily.csv')
                return daily_df
            else:
                print("No matching data found for the given date.")
                return pd.DataFrame()  # Return an empty DataFrame if no data is found

        except Exception as e:
            print("Error:", e)
            return pd.DataFrame()  # Return an empty DataFrame on error
        
    
    def __get_data_availability(self, df):
        variables = ['HourlyAltimeterSetting','HourlyDewPointTemperature','HourlyDryBulbTemperature','HourlyPrecipitation','HourlyPresentWeatherType','HourlyPressureChange','HourlyPressureTendency','HourlyRelativeHumidity','HourlySkyConditions','HourlySeaLevelPressure','HourlyStationPressure','HourlyVisibility','HourlyWetBulbTemperature','HourlyWindDirection']
        grouped_df = df.groupby("NAME")[variables].count()

        # Plot heatmap
        plt.figure(figsize=(14, 6))
        sns.heatmap(grouped_df, cmap="RdYlGn", annot=True, linewidths=0.5)

        plt.xlabel("Variables")
        plt.ylabel("Weather Stations")
        plt.title("Data Availability Heatmap")

        plt.xticks(rotation=45, ha="right", fontsize=10)  # Rotate for readability
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.savefig('data_avail.png')
        

    @staticmethod
    def clear_cache(cache_dir: Optional[str] = None):
        """
        Utility method to clear the entire cache
        """
        cache_dir = cache_dir or os.path.expanduser('~/.weather_cache')
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            os.makedirs(cache_dir)
            logging.info(f"Cache cleared: {cache_dir}")

    def __get_url(self, location_box):
        north = str(location_box[1]) + ","
        west = str(location_box[2]) + ","
        south = str(location_box[0]) + ","
        east = location_box[3]
        
        urls = []
        base_url = (
            "https://www.ncei.noaa.gov/access/search/data-search/local-climatological-data"
            f"?bbox={north}{west}{south}{east}"
            f"&startDate={self.date}T00:00:00&endDate={self.end_date}T23:59:59"
        )
        print(base_url)
        full_url = base_url + "&pageNum=1"

        # Set up headless Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(full_url)
            time.sleep(3)  # Give time for JS to render

            # Get full page source after JS execution
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find pagination text like "Page 1 of 2"
            page_info = soup.find(string=re.compile(r"Page\s+\d+\s+of\s+\d+"))
            if not page_info:
                # raise Exception("Pagination text not found. Page may not have loaded properly.")
                return [full_url]

            match = re.search(r"Page\s+\d+\s+of\s+(\d+)", page_info)
            if not match:
                raise Exception("Failed to parse total page count.")

            total_pages = int(match.group(1))

            # Generate all URLs
            for page_num in range(1, total_pages + 1):
                page_url = base_url + f"&pageNum={page_num}"
                urls.append(page_url)

        finally:
            driver.quit()
        print(urls)
        return urls
    
    def __get_AQI_url(self, location_box):
        """Modified to use environment variable for AirNow API key"""
        north = location_box[1]
        west = location_box[2]
        south = location_box[0]
        east = location_box[3]
        url = f"https://www.airnowapi.org/aq/data/?startDate={self.date}T0&endDate={self.date}T23&parameters=OZONE,PM25,PM10,CO,NO2,SO2&BBOX={west},{south},{east},{north}&dataType=B&format=application/json&verbose=1&monitorType=2&includerawconcentrations=1&API_KEY={self.airnow_api_key}"
        return url
    
    def __create_links(self, urls):
        links_set = []
        for url in urls:
            self.driver.get(url)  # Ensure page is fully reloaded
            # throw exception if url/NOAA is down
            self.driver.refresh()  # Force refresh to avoid caching issues

            try:
                # Wait for the elements to load
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-header")))
                for link in self.driver.find_elements(By.CSS_SELECTOR, ".card-header a"):
                    # if len(links_set) >= self.n:
                    #     break  # Stop once we have the max number of links
                    if link.get_attribute("href") not in links_set:
                        links_set.append(link.get_attribute("href"))
                
            except Exception as e:
                print(e)
        
        # Close the browser
        self.driver.quit()
        print(str(len(links_set)) + " csv links found")
        return links_set

    def __fetch_and_process_csv(self, url):
        try:
            # Fetch CSV content
            response = requests.get(url)
            
            if response.status_code == 200:
                # Read CSV content directly into a DataFrame
                csv_content = StringIO(response.text)
                df = pd.read_csv(csv_content, low_memory=False)
                return df
            else:
                print(f"Failed to fetch {url}, status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def __fetch_all_data(self, links_set):
        dfs = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Map the URLs to fetch_and_process_csv function
            future_to_url = {executor.submit(self.__fetch_and_process_csv, l): l for l in links_set}
            
            # Wait for all futures to complete
            for future in as_completed(future_to_url):
                result = future.result()
                if result is not None:
                    dfs.append(result)
        
        return dfs

    def __get_links(self):
        location_box = self.__setup()
        url = self.__get_url(location_box)
        links = self.__create_links(url)
        return links

    def __setup(self):
        """Modified to use environment variable for Nominatim user agent"""
        geolocator = Nominatim(user_agent=self.nominatim_user_agent)
        location = geolocator.geocode(self.city, exactly_one=True)
        if location:
            location_box = location.raw['boundingbox']
            return location_box
        else:
            raise Exception("Location not found. Please check city name.")

    def __get_hourly_range(self, links_set):
        try:
            # Convert the DATE column to datetime format if it isn't already
            if not pd.api.types.is_datetime64_any_dtype(self.yearly_df['DATE']):
                self.yearly_df['DATE'] = pd.to_datetime(self.yearly_df['DATE'])

            # Filter rows within the date range
            mask = (self.yearly_df['DATE'] >= self.date) & (self.yearly_df['DATE'] <= self.end_date)
            filtered_df = self.yearly_df[mask]

            print(f"Filtered {len(filtered_df)} rows within the date range {self.date} to {self.end_date}.")
            filtered_df.to_csv("dateRangeContent.csv")
            return filtered_df

        except Exception as e:
            print("Error:", e)
            return pd.DataFrame()


    def __get_AQI(self):
        location_box = self.__setup()
        url = self.__get_AQI_url(location_box)
        response = requests.get(url)
        if response.status_code == 200:
            aqi_list = response.json()
            if (len(aqi_list) > 0):
                aqi_string = str(aqi_list)
                aqi_string = aqi_string.replace("'", '"')
                json_data = json.loads(aqi_string)
                csv_file = 'AQI.csv'
                csv_obj = open(csv_file, 'w')
                csv_writer = csv.writer(csv_obj)
                header = json_data[0].keys()
                csv_writer.writerow(header)
                for item in json_data:
                    csv_writer.writerow(item.values())
                csv_obj.close()


    def generate_hourly_data(self):
        links = self.__get_links()
        self.__get_yearly_content(links)
        self.__get_daily_content(links)
    
    def generate_yearly_hourly_data(self):
        links = self.__get_links()
        self.__get_yearly_content(links)
        self.yearly_df.to_csv("yearlyContent.csv")


    def generate_hourly_data_range(self):
        links = self.__get_links()
        self.__get_yearly_content(links)
        self.__get_hourly_range(links)
            

    def generate_AQI_data(self):
        self.__get_AQI()


# Example usage with custom cache configuration
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("city", type=str, help="Enter the city or state")
    parser.add_argument("date", type=str, help="Enter the date (YYYY-MM-DD)")
    parser.add_argument('--endDate', type=str, default=None, help="Enter the optional end date (YYYY-MM-DD)")
    parser.add_argument('--v', type=bool, default=False, help="Enter if you'd like a visualization")
    parser.add_argument('--cache-dir', type=str, help="Custom cache directory path")
    parser.add_argument('--max-cache-age', type=int, help="Maximum cache age in days")
    parser.add_argument('--max-cache-size', type=float, help="Maximum cache size in GB")
    parser.add_argument('--init-env', action='store_true', help="Initialize .env file template")
    args = parser.parse_args()

    if args.init_env:
        # Create .env template if it doesn't exist
        if not os.path.exists('.env'):
            with open('.env', 'w') as f:
                f.write("# AirNow API Key (Required)\n")
                f.write("AIRNOW_API_KEY=your_airnow_api_key_here\n\n")
                f.write("# Nominatim User Agent (Required)\n")
                f.write("NOMINATIM_USER_AGENT=your_unique_user_agent_here\n")
            print("Created .env template file. Please fill in your API credentials.")
            sys.exit(0)

    try:
        # Prepare cache configuration
        cache_config = {}
        if args.cache_dir:
            cache_config['cache_dir'] = args.cache_dir
        if args.max_cache_age:
            cache_config['max_age_days'] = args.max_cache_age
        if args.max_cache_size:
            cache_config['max_cache_size_gb'] = args.max_cache_size

        w = Weather(args.date, args.city, args.endDate, cache_config=cache_config)
        if args.endDate != None and args.date != args.endDate:
            w.generate_hourly_data_range()
        else:
            w.generate_hourly_data()
    except Exception as e:
        print(f"Error: {e}")
        if "No .env file found" in str(e):
            print("\nTo create a .env template, run: python mainWeather.py --init-env")


if __name__ == '__main__':
    main()
import requests
import json
import os

def fetch_data_for_year(year):
    base_url = "http://ergast.com/api/f1"
    endpoints = {
        'race_info': f"{base_url}/{year}.json",
        'race_results': f"{base_url}/{year}/results.json",
        'qualifying_results': f"{base_url}/{year}/qualifying.json",
        'driver_standings': f"{base_url}/{year}/driverStandings.json",
        'constructor_standings': f"{base_url}/{year}/constructorStandings.json",
        'status': f"{base_url}/{year}/status.json",
    }

    # Include sprint qualifying results for applicable years
    if year >= 2021:
        endpoints['sprint_qualifying_results'] = f"{base_url}/{year}/sprint/qualifying.json"

    year_data = {}
    for data_type, url in endpoints.items():
        response = requests.get(url)
        if response.status_code == 200:
            year_data[data_type] = response.json()
        else:
            print(f"Failed to fetch {data_type} for {year}")

    return year_data

def save_data(data, folder_name, data_type):
    folder_path = f"data/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = f"{folder_path}/{data_type}.json"
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    for year in range(2001, 2025):
        print(f"Fetching data for {year}...")
        year_data = fetch_data_for_year(year)
        for data_type, data in year_data.items():
            save_data(data, str(year), data_type)
        print(f"Data for {year} fetched and saved.")

if __name__ == "__main__":
    main()

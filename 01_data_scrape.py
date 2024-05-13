import requests
import json
import os

def fetch_races(year):
    base_url = f"http://ergast.com/api/f1/{year}.json"
    response = requests.get(base_url)
    if response.status_code == 200:
        races = response.json()['MRData']['RaceTable']['Races']
        return [(race['round'], race['raceName']) for race in races]
    else:
        print(f"Failed to fetch races for {year}")
        return []

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['MRData']['RaceTable']['Races']:  # Check if the 'Races' list is not empty
            return data
    return None

def save_data(data, folder_name, data_type):
    folder_path = f"data/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = f"{folder_path}/{data_type}.json"
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def data_exists(folder_name, data_type):
    folder_path = f"data/{folder_name}"
    file_path = f"{folder_path}/{data_type}.json"
    return os.path.exists(file_path)

def main():
    for year in range(2001, 2025):
        print(f"Fetching data for {year}...")
        races = fetch_races(year)
        for index, (round, race_name) in enumerate(races, start=1):
            folder_name = f"{year}/{index:02d}-{race_name}"
            race_results_url = f"http://ergast.com/api/f1/{year}/{round}/results.json"
            qualifying_url = f"http://ergast.com/api/f1/{year}/{round}/qualifying.json"
            sprint_results_url = f"http://ergast.com/api/f1/{year}/{round}/sprint/results.json"
            sprint_qualifying_url = f"http://ergast.com/api/f1/{year}/{round}/sprint/qualifying.json"

            # Standard race results
            race_results = fetch_data(race_results_url)
            if race_results:
                save_data(race_results, folder_name, "race_results")

            # Standard qualifying results
            qualifying = fetch_data(qualifying_url)
            if qualifying:
                save_data(qualifying, folder_name, "quali_results")

            # Sprint race results
            if year >= 2021:
                sprint_results = fetch_data(sprint_results_url)
                if sprint_results:
                    save_data(sprint_results, folder_name, "sprint_race_results")

                sprint_qualifying = fetch_data(sprint_qualifying_url)
                if sprint_qualifying:
                    save_data(sprint_qualifying, folder_name, "sprint_quali_results")

if __name__ == "__main__":
    main()

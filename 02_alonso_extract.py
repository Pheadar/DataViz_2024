import json
import os

def extract_alonso_data(start_year, end_year):
    alonso_data = {}

    for year in range(start_year, end_year + 1):
        file_path = f"data/{year}/driver_standings.json"
        if not os.path.exists(file_path):
            continue
        with open(file_path, 'r') as file:
            data = json.load(file)
            standings_list = data['MRData']['StandingsTable']['StandingsLists']
            if standings_list:
                standings = standings_list[0]['DriverStandings']
                for standing in standings:
                    if standing['Driver']['driverId'] == 'alonso':
                        alonso_data[year] = {
                            'position': standing['position'],
                            'points': standing['points']
                        }
                        break
    return alonso_data

alonso_data = extract_alonso_data(2001, 2024)
with open('treated_data/alonso_career_data.json', 'w') as f:
    json.dump(alonso_data, f, indent=4)
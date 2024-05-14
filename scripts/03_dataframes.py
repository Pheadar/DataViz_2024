import pandas as pd
import json, os, re, requests
from bs4 import BeautifulSoup

treated_data = os.path.join(os.curdir, 'treated_data')


def get_course_length(url, index, total):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the infobox table on the Wikipedia page
        infobox = soup.find('table', class_='infobox')
        if infobox:
            rows = infobox.find_all('tr')
            for row in rows:
                header = row.find('th')
                if header and 'Course length' in header.text:
                    length_text = row.find('td').text.strip()
                    # Remove any content in brackets
                    length_text = re.sub(r'\[.*?\]', '', length_text)
                    # Extract the kilometers part and clean it
                    km_match = re.search(r'(\d+[.,]?\d*)\s*km', length_text)
                    if km_match:
                        km_cleaned = km_match.group(1).replace(',', '.')
                        print(f"Processed {index + 1}/{total} races")
                        return float(km_cleaned)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {str(e)}")
    print(f"Processed {index + 1}/{total} races ({url}): No course length found.")
    return None



with open(f"{treated_data}{os.sep}all_race_results.json") as file:
    data = json.load(file)



drivers = []
for result in data:
    season = result['MRData']['RaceTable']['season']
    round = result['MRData']['RaceTable']['round']
    for race in result['MRData']['RaceTable']['Races']:
        for result in race['Results']:
            driver_result = {
                'driverId': result['Driver']['driverId'],
                'driverCode': result['Driver'].get('code', 'N/A'),
                'driverName': result['Driver']['givenName'] + ' ' + result['Driver']['familyName'],
                'driverNationality': result['Driver']['nationality'],
                'dob': result['Driver']['dateOfBirth'],
            }
            drivers.append(driver_result)
driver_info = pd.DataFrame(drivers)
driver_info = driver_info.drop_duplicates(subset='driverId')



teams = []
for result in data:
    season = result['MRData']['RaceTable']['season']
    round = result['MRData']['RaceTable']['round']
    for race in result['MRData']['RaceTable']['Races']:
        for result in race['Results']:
            team_result = {
                'teamId': result['Constructor']['constructorId'],
                'team': result['Constructor']['name'],
                'teamNationality': result['Constructor']['nationality'],
                'url': result['Constructor']['url'] if 'url' in result['Constructor'] else 'N/A',
            }
            teams.append(team_result)
team_info = pd.DataFrame(teams)
team_info = team_info.drop_duplicates(subset='teamId')



races = []
for result in data:
    season = result['MRData']['RaceTable']['season']
    round = result['MRData']['RaceTable']['round']
    for race in result['MRData']['RaceTable']['Races']:
        race_data = {
            'season': season,
            'round': round,
            'raceName': race['raceName'],
            'raceId': race['raceName'] + ' ' + season,
            'url': race['url'],
            'date': race['date'],
            'circuitId': race['Circuit']['circuitId'],
        }
        races.append(race_data)
race_info = pd.DataFrame(races)
race_info = race_info.drop_duplicates(subset=['circuitId', 'date'])

total_number = race_info.shape[0]
print(f"Starting to find course length for {total_number} races...")

course_lengths = []
for idx, row in race_info.iterrows():
    course_length = get_course_length(row['url'], idx, total_number)
    course_lengths.append(course_length)

race_info['course_length_km'] = course_lengths



circuits = []
for result in data:
    season = result['MRData']['RaceTable']['season']
    round = result['MRData']['RaceTable']['round']
    for race in result['MRData']['RaceTable']['Races']:
        for result in race['Results']:
            circuit_info = {
                'circuitId': race['Circuit']['circuitId'],
                'url': race['Circuit']['url'],
                'circuitName': race['Circuit']['circuitName'],
                'latitude': race['Circuit']['Location']['lat'],
                'longitude': race['Circuit']['Location']['long'],
                'location': race['Circuit']['Location']['locality'],
                'country': race['Circuit']['Location']['country'],
            }
            circuits.append(circuit_info)
circuit_info = pd.DataFrame(circuits)
circuit_info = circuit_info.drop_duplicates(subset='circuitId')



results = []
for result in data:
    season = result['MRData']['RaceTable']['season']
    round = result['MRData']['RaceTable']['round']
    for race in result['MRData']['RaceTable']['Races']:
        raceId = race['raceName'] + ' ' + season
        raceUrl = race['url']
        raceDate = race['date']
        circuitId = race['Circuit']['circuitId']
        for result in race['Results']:
            result_info = {
                'season': season,
                'round': round,
                'raceId': raceId,
                'circuitId': circuitId,
                'driverId': result['Driver']['driverId'],
                'constructorId': result['Constructor']['constructorId'],
                'grid': int(result['grid']),
                'position': int(result['position']),
                'positionText': result['positionText'],
                'points': float(result['points']),
                'laps': int(result['laps']),
                'status': result['status'],
                'timeMillis': result['Time']['millis'] if 'Time' in result else None,
                'time': result['Time']['time'] if 'Time' in result else None
            }
            results.append(result_info)
race_results = pd.DataFrame(results)


pickles_folder = os.path.join(treated_data, 'pickles')
csv_folder = os.path.join(treated_data, 'csv')
driver_info.to_pickle(os.path.join(pickles_folder, 'driver_info.pkl'))
driver_info.to_csv(os.path.join(csv_folder, 'driver_info.csv'), index=False)
team_info.to_pickle(os.path.join(pickles_folder, 'team_info.pkl'))
team_info.to_csv(os.path.join(csv_folder, 'team_info.csv'), index=False)
race_info.to_pickle(os.path.join(pickles_folder, 'race_info.pkl'))
race_info.to_csv(os.path.join(csv_folder, 'race_info.csv'), index=False)
circuit_info.to_pickle(os.path.join(pickles_folder, 'circuit_info.pkl'))
circuit_info.to_csv(os.path.join(csv_folder, 'circuit_info.csv'), index=False)
race_results.to_pickle(os.path.join(pickles_folder, 'results.pkl'))
race_results.to_csv(os.path.join(csv_folder, 'results.csv'), index=False)
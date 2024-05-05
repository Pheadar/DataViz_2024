import pandas as pd
import json
import os

def get_json_files(directory, file_suffix):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_suffix):
                json_files.append(os.path.join(root, file))
    return json_files

def process_json_file(file_path, file_type):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        
        if file_type in ['constructor_standings.json', 'driver_standings.json'] and 'StandingsTable' in json_data['MRData']:
            return process_standings(json_data)
        
        if file_type == 'qualifying_results.json' and 'RaceTable' in json_data['MRData']:
            return process_qualifying(json_data)
        
        if file_type == 'race_results.json' and 'RaceTable' in json_data['MRData']:
            return process_race_results(json_data)
        
        if file_type == 'race_info.json' and 'RaceTable' in json_data['MRData']:
            return process_race_info(json_data)

        print(f"Skipped file {file_path} due to missing necessary data key")
    return pd.DataFrame()

def process_standings(json_data):
    standings_lists = json_data['MRData']['StandingsTable']['StandingsLists']
    data_frames = []
    for standings in standings_lists:
        if 'ConstructorStandings' in standings:
            df = pd.json_normalize(standings, record_path='ConstructorStandings',
                                   meta=['season', 'round'],
                                   errors='ignore')
        elif 'DriverStandings' in standings:
            df = pd.json_normalize(standings, record_path='DriverStandings',
                                   meta=['season', 'round'],
                                   errors='ignore')
        data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()

def process_qualifying(json_data):
    races = json_data['MRData']['RaceTable']['Races']
    data_frames = []
    for race in races:
        if 'QualifyingResults' in race:
            df = pd.json_normalize(race, record_path='QualifyingResults',
                                   meta=['season', 'round', 'raceName', ['Circuit', 'circuitId'], ['Circuit', 'circuitName'],
                                         ['Circuit', 'Location', 'locality'], ['Circuit', 'Location', 'country'],
                                         'date'],
                                   errors='ignore')
            data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()

def process_race_results(json_data):
    races = json_data['MRData']['RaceTable']['Races']
    data_frames = []
    for race in races:
        if 'Results' in race:
            df = pd.json_normalize(race, record_path='Results',
                                   meta=[
                                       'season', 'round', 'raceName', ['Circuit', 'circuitId'],
                                       ['Circuit', 'circuitName'], ['Circuit', 'Location', 'locality'],
                                       ['Circuit', 'Location', 'country'], 'date',
                                       ['Time', 'time'], ['Time', 'millis']],
                                   errors='ignore',
                                   record_prefix='Result_')
            data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()

def process_race_info(json_data):
    races = json_data['MRData']['RaceTable']['Races']
    df = pd.json_normalize(races, sep='_',
                           record_path=None,
                           meta=['season', 'round', 'raceName', 'date', 
                                 ['Circuit', 'circuitId'], ['Circuit', 'circuitName'], 
                                 ['Circuit', 'url'], 
                                 ['Circuit', 'Location', 'lat'], ['Circuit', 'Location', 'long'],
                                 ['Circuit', 'Location', 'locality'], ['Circuit', 'Location', 'country']])
    return df

def save_data(data_dict):
    for key, df in data_dict.items():
        output_file = f'treated_data/merged_{key}.csv'
        if not df.empty:
            if output_file.endswith('.csv'):
                df.to_csv(output_file, index=False)
            elif output_file.endswith('.json'):
                df.to_json(output_file, orient='records', lines=True)
            print(f"Data saved to {output_file}")
        else:
            print(f"No data to save for {key}.")

def main():
    data_dir = 'data'
    file_types = {
        'constructor_standings.json': 'constructor_standings',
        'driver_standings.json': 'driver_standings',
        'qualifying_results.json': 'qualifying_results',
        'race_results.json': 'race_results',
        'race_info.json': 'race_info'
    }
    
    data_dict = {value: pd.DataFrame() for value in file_types.values()}
    
    for file_suffix, data_key in file_types.items():
        json_files = get_json_files(data_dir, file_suffix)
        for json_file in json_files:
            df = process_json_file(json_file, file_suffix)
            data_dict[data_key] = pd.concat([data_dict[data_key], df], ignore_index=True)
    
    save_data(data_dict)

if __name__ == "__main__":
    main()
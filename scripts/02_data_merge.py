import os
import json

def combine_json_files(data_type):
    base_path = os.path.join(os.curdir, 'data')
    all_data = []
    for year in os.listdir(base_path):
        year_path = os.path.join(base_path, year)
        if os.path.isdir(year_path):
            for race in os.listdir(year_path):
                race_path = os.path.join(year_path, race)
                json_file_path = os.path.join(race_path, f"{data_type}.json")
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r') as file:
                        data = json.load(file)
                        all_data.append(data)
    return all_data

def save_data_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def main():
    if not os.path.exists(os.path.join(os.curdir, 'treated_data')):
        os.makedirs(os.path.join(os.curdir, 'treated_data'))
        
    # race results
    all_race_results = combine_json_files('race_results')
    save_data_to_json(all_race_results, f"{os.path.join(os.curdir, 'treated_data')}{os.sep}all_race_results.json")

    # qualifying results
    all_quali_results = combine_json_files('quali_results')
    save_data_to_json(all_quali_results, f"{os.path.join(os.curdir, 'treated_data')}{os.sep}all_quali_results.json")


if __name__ == "__main__":
    main()
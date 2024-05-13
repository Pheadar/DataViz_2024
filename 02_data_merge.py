import os
import json

def combine_json_files(data_type):
    base_path = 'data'
    all_data = []
    # Traverse the directory structure
    for year in os.listdir(base_path):
        year_path = os.path.join(base_path, year)
        if os.path.isdir(year_path):
            for race in os.listdir(year_path):
                race_path = os.path.join(year_path, race)
                json_file_path = os.path.join(race_path, f"{data_type}.json")
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r') as file:
                        data = json.load(file)
                        # Append the loaded data to the all_data list
                        all_data.append(data)

    return all_data

def save_data_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def main():
    # Combine race results into a single JSON file
    all_race_results = combine_json_files('race_results')
    save_data_to_json(all_race_results, 'all_race_results.json')

    # Combine qualifying results into a single JSON file
    all_quali_results = combine_json_files('quali_results')
    save_data_to_json(all_quali_results, 'all_quali_results.json')

if __name__ == "__main__":
    main()

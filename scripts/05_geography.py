import pandas as pd
import os

# Load data
base_path = os.path.join(os.curdir, 'treated_data')
race_results = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'results.pkl'])))
race_info = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'race_info.pkl'])))
circuit_info = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'circuit_info.pkl'])))

# Print columns of each DataFrame to debug
print("race_results columns:", race_results.columns)
print("race_info columns:", race_info.columns)
print("circuit_info columns:", circuit_info.columns)

# Seasons to filter
selected_seasons = [2005, 2006]

# Filter races for the selected driver (Fernando Alonso) and the specified seasons
alonso_results = race_results[(race_results['driverId'] == 'alonso') & (race_results['season'].isin(selected_seasons))]

# Merge the filtered race data with race information to get circuit IDs
merged_data = alonso_results.merge(race_info, on='raceId')

# Merge the result with circuit information to get location data
location_data = merged_data.merge(circuit_info, on='circuitId')

# Select relevant columns
location_data = location_data[['season', 'round', 'raceName', 'date', 'circuitName', 'latitude', 'longitude', 'location', 'country']]

# Sort by season and round
location_data = location_data.sort_values(by=['season', 'round']).reset_index(drop=True)

# Save to dataframe
output_path_csv = os.path.join(base_path, 'csv', 'alonso_race_locations_2005_2006.csv')
output_path_pickle = os.path.join(base_path, 'pickles', 'alonso_race_locations_2005_2006.pkl')

if isinstance(location_data, pd.DataFrame):
    location_data.to_csv(output_path_csv, index=False)
    location_data.to_pickle(output_path_pickle)

# Display the first few rows of the final DataFrame for verification
print(location_data.head())


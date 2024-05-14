import os
import pandas as pd

# Define the base path and load the dataframes from pickle files
base_path = os.path.join(os.curdir, 'treated_data')
circuit_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'circuit_info.pkl'))
driver_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'driver_info.pkl'))
race_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'race_info.pkl'))
results = pd.read_pickle(os.path.join(base_path, 'pickles', 'results.pkl'))
team_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'team_info.pkl'))

# Convert 'season' and 'round' columns to integer
race_info['season'] = race_info['season'].astype(int)
race_info['round'] = race_info['round'].astype(int)
results['season'] = results['season'].astype(int)
results['round'] = results['round'].astype(int)

# Check the contents of race_info
print("Contents of race_info DataFrame after type conversion:")
print(race_info.head())
print(race_info.info())

# Filter the race_info and results for the 2005 and 2006 seasons
races_2005 = race_info[race_info['season'] == 2005]
races_2006 = race_info[race_info['season'] == 2006]
results_2005 = results[results['season'] == 2005]
results_2006 = results[results['season'] == 2006]

# Print the filtered data to verify
print("Filtered races for 2005 season:")
print(races_2005)
print("Filtered races for 2006 season:")
print(races_2006)

print("Filtered results for 2005 season:")
print(results_2005)
print("Filtered results for 2006 season:")
print(results_2006)

# Merge the race information with circuit information
def merge_race_circuit_info(races):
    return races.merge(circuit_info, on='circuitId', how='left')

races_2005_merged = merge_race_circuit_info(races_2005)
races_2006_merged = merge_race_circuit_info(races_2006)

# Select the required columns for the final race dataframes
columns_needed = ['round', 'raceId', 'date', 'latitude', 'longitude', 'raceName']

races_2005_final = races_2005_merged[columns_needed]
races_2006_final = races_2006_merged[columns_needed]

# Print the final dataframes to verify
print("2005 races after merging with circuit info:")
print(races_2005_final)
print("2006 races after merging with circuit info:")
print(races_2006_final)

# Merge results with race_info to get the date column
results_2005 = results_2005.merge(race_info[['raceId', 'date']], on='raceId', how='left')
results_2006 = results_2006.merge(race_info[['raceId', 'date']], on='raceId', how='left')

# Print the merged results to verify
print("Merged results for 2005 season:")
print(results_2005)
print("Merged results for 2006 season:")
print(results_2006)

# Function to calculate cumulative points for a season
def calculate_cumulative_points(results, season):
    results_sorted = results.sort_values(by=['date', 'round'])
    results_sorted['cumulativePoints'] = results_sorted.groupby('driverId')['points'].cumsum()
    results_sorted = results_sorted.merge(driver_info[['driverId', 'driverName']], on='driverId')
    results_sorted = results_sorted[['round', 'raceId', 'driverId', 'driverName', 'position', 'points', 'cumulativePoints']]
    results_sorted.rename(columns={'position': 'raceFinalPosition', 'points': 'racePoints'}, inplace=True)
    return results_sorted

# Calculate cumulative points for 2005 and 2006
cumulative_points_2005 = calculate_cumulative_points(results_2005, 2005)
cumulative_points_2006 = calculate_cumulative_points(results_2006, 2006)

# Save the final dataframes
races_2005_final.to_pickle(os.path.join(base_path, 'pickles', '2005_races.pkl'))
races_2006_final.to_pickle(os.path.join(base_path, 'pickles', '2006_races.pkl'))
races_2005_final.to_csv(os.path.join(base_path, 'csv', '2005_races.csv'), index=False)
races_2006_final.to_csv(os.path.join(base_path, 'csv', '2006_races.csv'), index=False)
cumulative_points_2005.to_pickle(os.path.join(base_path, 'pickles', '2005_cumulative_points.pkl'))
cumulative_points_2006.to_pickle(os.path.join(base_path, 'pickles', '2006_cumulative_points.pkl'))
cumulative_points_2005.to_csv(os.path.join(base_path, 'csv', '2005_cumulative_points.csv'), index=False)
cumulative_points_2006.to_csv(os.path.join(base_path, 'csv', '2006_cumulative_points.csv'), index=False)

# Print to verify
print("2005 Races DataFrame:")
print(races_2005_final.head())

print("2006 Races DataFrame:")
print(races_2006_final.head())

print("2005 Cumulative Points DataFrame:")
print(cumulative_points_2005.head())

print("2006 Cumulative Points DataFrame:")
print(cumulative_points_2006.head())

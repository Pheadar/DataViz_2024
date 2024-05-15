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

# Filter the race_info and results for the 2005 and 2006 seasons
races_2005 = race_info[race_info['season'] == 2005]
races_2006 = race_info[race_info['season'] == 2006]
results_2005 = results[results['season'] == 2005]
results_2006 = results[results['season'] == 2006]

# Merge results with team_info to get the constructorId
results_2005 = results_2005.merge(team_info[['teamId']], left_on='constructorId', right_on='teamId', how='left')
results_2006 = results_2006.merge(team_info[['teamId']], left_on='constructorId', right_on='teamId', how='left')

# Merge the race information with circuit information
def merge_race_circuit_info(races):
    return races.merge(circuit_info, on='circuitId', how='left')

races_2005_merged = merge_race_circuit_info(races_2005)
races_2006_merged = merge_race_circuit_info(races_2006)

# Select the required columns for the final race dataframes
columns_needed = ['round', 'raceId', 'date', 'latitude', 'longitude', 'raceName']

races_2005_final = races_2005_merged[columns_needed]
races_2006_final = races_2006_merged[columns_needed]

# Replace 'Grand Prix' with 'GP' in race names
races_2005_final['raceName'] = races_2005_final['raceName'].str.replace('Grand Prix', 'GP')
races_2006_final['raceName'] = races_2006_final['raceName'].str.replace('Grand Prix', 'GP')

# Merge results with race_info to get the date column
results_2005 = results_2005.merge(race_info[['raceId', 'date']], on='raceId', how='left')
results_2006 = results_2006.merge(race_info[['raceId', 'date']], on='raceId', how='left')

# Function to calculate cumulative points for a season
def calculate_cumulative_points(results, season):
    results_sorted = results.sort_values(by=['date', 'round'])
    results_sorted['cumulativePoints'] = results_sorted.groupby('driverId')['points'].cumsum()
    results_sorted = results_sorted.merge(driver_info[['driverId', 'driverName']], on='driverId')
    results_sorted.rename(columns={'position': 'raceFinalPosition', 'points': 'racePoints'}, inplace=True)
    results_sorted = results_sorted[['round', 'raceId', 'driverId', 'driverName', 'constructorId', 'raceFinalPosition', 'racePoints', 'cumulativePoints']]
    return results_sorted

# Calculate cumulative points for 2005 and 2006
cumulative_points_2005 = calculate_cumulative_points(results_2005, 2005)
cumulative_points_2006 = calculate_cumulative_points(results_2006, 2006)

# Pivot the dataframes to get the desired format
def pivot_cumulative_points(df, races):
    df_pivot = df.pivot_table(index=['driverId', 'driverName', 'constructorId'], columns='raceId', values='cumulativePoints', aggfunc='max').reset_index()
    race_names = races[['raceId', 'raceName']].drop_duplicates().set_index('raceId').to_dict()['raceName']
    df_pivot.rename(columns=race_names, inplace=True)
    race_order = races.sort_values(by='date')['raceName'].unique()
    df_pivot = df_pivot[['driverId', 'driverName', 'constructorId'] + list(race_order)]
    return df_pivot

# Add image URLs to specific drivers
def add_image_urls(df):
    image_urls = {
        'alonso': 'https://www.driverdb.com/_next/image?url=https%3A%2F%2Fassets.driverdb.com%2Fdrivers%2Fprofile%2F10_360d54b27fc33a0b352f.jpg&w=256&q=75',
        'michael_schumacher': 'https://www.driverdb.com/_next/image?url=https%3A%2F%2Fassets.driverdb.com%2Fdrivers%2Fprofile%2F1_144fcc31aaf89e9b4396.jpg&w=256&q=75',
        'massa': 'https://www.driverdb.com/_next/image?url=https%3A%2F%2Fassets.driverdb.com%2Fdrivers%2Fprofile%2F14_1e9df86fd1fd733f218c.jpg&w=256&q=75',
        'fisichella': 'https://www.driverdb.com/_next/image?url=https%3A%2F%2Fassets.driverdb.com%2Fdrivers%2Fprofile%2F13_fbda8a2efdd0b292f315.jpg&w=256&q=75',
        'raikkonen': 'https://www.driverdb.com/_next/image?url=https%3A%2F%2Fassets.driverdb.com%2Fdrivers%2Fprofile%2F8_feaf0ac16477c2ba6b54.jpg&w=256&q=75',
        'montoya': 'https://www.driverdb.com/_next/image?url=https%3A%2F%2Fassets.driverdb.com%2Fdrivers%2Fprofile%2F3_4920e25c1179e8cb4151.jpg&w=256&q=75'
    }
    df['image'] = df['driverId'].map(image_urls).fillna('')
    return df

# Pivot the cumulative points dataframes
pivot_2005 = pivot_cumulative_points(cumulative_points_2005, races_2005_final)
pivot_2006 = pivot_cumulative_points(cumulative_points_2006, races_2006_final)

# Sort the pivot dataframes by final championship position
def sort_by_final_position(df, cumulative_points):
    final_positions = cumulative_points.groupby('driverId')['cumulativePoints'].max().reset_index().sort_values(by='cumulativePoints', ascending=False)
    df_sorted = df.set_index('driverId').loc[final_positions['driverId']].reset_index()
    return df_sorted

pivot_2005 = sort_by_final_position(pivot_2005, cumulative_points_2005)
pivot_2006 = sort_by_final_position(pivot_2006, cumulative_points_2006)

# Add image URLs to the pivoted dataframes
pivot_2005 = add_image_urls(pivot_2005)
pivot_2006 = add_image_urls(pivot_2006)

# Reorder columns to place 'image' between 'driverName' and 'constructorId'
def reorder_columns(df):
    columns = df.columns.tolist()
    columns.insert(columns.index('constructorId'), columns.pop(columns.index('image')))
    return df[columns]

pivot_2005 = reorder_columns(pivot_2005)
pivot_2006 = reorder_columns(pivot_2006)

# Save the pivoted dataframes
pivot_2005.to_pickle(os.path.join(base_path, 'pickles', '2005_timeline.pkl'))
pivot_2006.to_pickle(os.path.join(base_path, 'pickles', '2006_timeline.pkl'))
pivot_2005.to_csv(os.path.join(base_path, 'csv', '2005_timeline.csv'), index=False)
pivot_2006.to_csv(os.path.join(base_path, 'csv', '2006_timeline.csv'), index=False)

# Function to create the shortened dataframes
def create_shortened_df(df, cumulative_points):
    top_5_drivers = cumulative_points.groupby('driverId')['cumulativePoints'].max().nlargest(5).index
    shortened_df = df[df['driverId'].isin(top_5_drivers)]
    return shortened_df

# Create the shortened dataframes for 2005 and 2006
shortened_2005 = create_shortened_df(pivot_2005, cumulative_points_2005)
shortened_2006 = create_shortened_df(pivot_2006, cumulative_points_2006)

# Save the shortened dataframes
shortened_2005.to_pickle(os.path.join(base_path, 'pickles', '2005_timeline_short.pkl'))
shortened_2006.to_pickle(os.path.join(base_path, 'pickles', '2006_timeline_short.pkl'))
shortened_2005.to_csv(os.path.join(base_path, 'csv', '2005_timeline_short.csv'), index=False)
shortened_2006.to_csv(os.path.join(base_path, 'csv', '2006_timeline_short.csv'), index=False)

# Print to verify
print("2005 Shortened Timeline DataFrame:")
print(shortened_2005.head())

print("2006 Shortened Timeline DataFrame:")
print(shortened_2006.head())

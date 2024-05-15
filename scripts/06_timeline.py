import os
import pandas as pd

# Define the base path and load the dataframes from pickle files
base_path = os.path.join(os.curdir, 'treated_data')
circuit_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'circuit_info.pkl'))
driver_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'driver_info.pkl'))
race_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'race_info.pkl'))
results = pd.read_pickle(os.path.join(base_path, 'pickles', 'results.pkl'))
team_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'team_info.pkl'))

# Load driver images
driver_images = pd.read_csv(os.path.join(base_path, 'csv', 'driver_photos.csv'))

# Convert 'season' and 'round' columns to integer
race_info['season'] = race_info['season'].astype(int)
race_info['round'] = race_info['round'].astype(int)
results['season'] = results['season'].astype(int)
results['round'] = results['round'].astype(int)

# Filter the race_info and results for the 2005 and 2006 seasons
seasons = [2005, 2006]

def load_season_data(season):
    season_race_info = race_info[race_info['season'] == season].copy()
    season_results = results[results['season'] == season].copy()
    
    # Merge results with team_info to get the constructorId
    season_results = season_results.merge(team_info[['teamId']], left_on='constructorId', right_on='teamId', how='left')
    
    # Merge the race information with circuit information
    season_race_info = season_race_info.merge(circuit_info, on='circuitId', how='left')
    
    # Select the required columns for the final race dataframes
    season_race_info = season_race_info[['round', 'raceId', 'date', 'latitude', 'longitude', 'raceName']].copy()
    
    # Replace 'Grand Prix' with 'GP' in race names
    season_race_info['raceName'] = season_race_info['raceName'].str.replace('Grand Prix', 'GP')
    
    # Merge results with race_info to get the date column
    season_results = season_results.merge(season_race_info[['raceId', 'date']], on='raceId', how='left')
    
    return season_race_info, season_results

def calculate_cumulative_points(results):
    results_sorted = results.sort_values(by=['date', 'round'])
    results_sorted.rename(columns={'points': 'racePoints'}, inplace=True)
    results_sorted['cumulativePoints'] = results_sorted.groupby('driverId')['racePoints'].cumsum()
    results_sorted = results_sorted.merge(driver_info[['driverId', 'driverName']], on='driverId')
    results_sorted = results_sorted[['round', 'raceId', 'driverId', 'driverName', 'constructorId', 'racePoints', 'cumulativePoints']]
    return results_sorted

def pivot_cumulative_points(df, races):
    race_names = races[['raceId', 'raceName', 'round']].drop_duplicates()
    race_names['raceLabel'] = race_names.apply(lambda x: f"{int(x['round']):02d} {x['raceName']}", axis=1)
    race_names_dict = race_names.set_index('raceId')['raceLabel'].to_dict()
    
    df_pivot = df.pivot_table(index=['driverId', 'driverName', 'constructorId'], columns='raceId', values='cumulativePoints', aggfunc='max').reset_index()
    df_pivot.rename(columns=race_names_dict, inplace=True)
    
    race_order = race_names.sort_values(by='round')['raceLabel'].unique()
    final_columns = ['driverId', 'driverName', 'constructorId'] + list(race_order)
    
    missing_columns = set(final_columns) - set(df_pivot.columns)
    for col in missing_columns:
        df_pivot[col] = None
    
    df_pivot = df_pivot[final_columns]
    return df_pivot

def add_driver_images(df):
    df = df.merge(driver_images, left_on='driverId', right_on='driverId', how='left')
    df['image'] = df['link']
    df.drop(columns=['link'], inplace=True)
    return df

def sort_by_final_position(df, cumulative_points):
    final_positions = cumulative_points.groupby('driverId')['cumulativePoints'].max().reset_index().sort_values(by='cumulativePoints', ascending=False)
    df_sorted = df.set_index('driverId').loc[final_positions['driverId']].reset_index()
    return df_sorted

def create_shortened_df(df, cumulative_points):
    top_5_drivers = cumulative_points.groupby('driverId')['cumulativePoints'].max().nlargest(5).index
    shortened_df = df[df['driverId'].isin(top_5_drivers)]
    return shortened_df

def create_sorted_drivers_df(results, races):
    results_sorted = results.merge(races[['raceId', 'raceName', 'date', 'latitude', 'longitude']], on='raceId', how='left')
    results_sorted = results_sorted[['driverId', 'raceName', 'racePoints', 'cumulativePoints', 'date', 'latitude', 'longitude']]
    results_sorted.rename(columns={'date': 'raceDate', 'latitude': 'raceLatitude', 'longitude': 'raceLongitude'}, inplace=True)
    return results_sorted

for season in seasons:
    season_race_info, season_results = load_season_data(season)
    cumulative_points = calculate_cumulative_points(season_results)
    
    # Timeline dataframe
    pivot_df = pivot_cumulative_points(cumulative_points, season_race_info)
    pivot_df = add_driver_images(pivot_df)
    pivot_df = sort_by_final_position(pivot_df, cumulative_points)
    pivot_df.to_pickle(os.path.join(base_path, 'pickles', f'{season}_timeline.pkl'))
    pivot_df.to_csv(os.path.join(base_path, 'csv', f'{season}_timeline.csv'), index=False)
    
    # Timeline short dataframe
    shortened_df = create_shortened_df(pivot_df, cumulative_points)
    shortened_df.to_pickle(os.path.join(base_path, 'pickles', f'{season}_timeline_short.pkl'))
    shortened_df.to_csv(os.path.join(base_path, 'csv', f'{season}_timeline_short.csv'), index=False)
    
    # Sorted drivers dataframe
    sorted_drivers_df = create_sorted_drivers_df(cumulative_points, season_race_info)
    sorted_drivers_df = sorted_drivers_df.sort_values(by='raceDate')
    sorted_drivers_df = sort_by_final_position(sorted_drivers_df, cumulative_points)
    sorted_drivers_df = add_driver_images(sorted_drivers_df)
    sorted_drivers_df.to_pickle(os.path.join(base_path, 'pickles', f'{season}_sorted_drivers.pkl'))
    sorted_drivers_df.to_csv(os.path.join(base_path, 'csv', f'{season}_sorted_drivers.csv'), index=False)

    # Print to verify
    print(f"{season} Timeline DataFrame:")
    print(pivot_df.head())

    print(f"{season} Shortened Timeline DataFrame:")
    print(shortened_df.head())

    print(f"{season} Sorted Drivers DataFrame:")
    print(sorted_drivers_df.head())

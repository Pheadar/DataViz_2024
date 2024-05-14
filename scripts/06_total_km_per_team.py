import pandas as pd
import os

# Load data
base_path = os.path.join(os.curdir, 'treated_data')
career_summary = pd.read_csv(os.path.join(base_path, 'alonso_career_summary.csv'))
race_results = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'results.pkl'])))
race_info = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'race_info.pkl'])))
team_info = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'team_info.pkl'])))

def race_distance(raceId):
    # Returns race distance by multiplying the number of laps by the circuit length
    race = race_info[race_info['raceId'] == raceId].iloc[0]
    return race['course_length_km']

def total_km_per_team():
    # Filter race results for the selected driver
    alonso_results = race_results[race_results['driverId'] == 'alonso']
    
    # Merge race results with race info to get the course length
    merged_data = alonso_results.merge(race_info, on='raceId')
    
    # Calculate distance for each race
    merged_data['race_distance'] = merged_data['laps'] * merged_data['course_length_km']
    
    # Group by constructorId and sum the distances
    km_per_team = merged_data.groupby('constructorId')['race_distance'].sum().reset_index()
    
    # Merge with team info to get team names
    km_per_team = km_per_team.merge(team_info[['teamId', 'team']], left_on='constructorId', right_on='teamId')

    # Merge with career summary to get the order of teams
    km_per_team = km_per_team.merge(career_summary[['constructor', 'startSeason']], left_on='team', right_on='constructor')
    
    # Select relevant columns and sort by startSeason to maintain the order
    km_per_team = km_per_team[['constructor', 'race_distance', 'startSeason']].rename(columns={'constructor': 'Team', 'race_distance': 'Total Distance (km)'})
    km_per_team = km_per_team.sort_values(by='startSeason').reset_index(drop=True)
    
    return km_per_team

# Save to dataframe
total_km = total_km_per_team()

if isinstance(total_km, pd.DataFrame):
    total_km.to_csv(os.path.join(base_path, 'csv', 'total_km_per_team.csv'), index=False)
    total_km.to_pickle(os.path.join(base_path, 'pickles', 'total_km_per_team.pkl'))

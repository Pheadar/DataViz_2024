import pandas as pd
import os

# Load data
base_path = os.path.join(os.curdir, 'treated_data')
career_summary = pd.read_csv(os.path.join(base_path, 'alonso_career_summary.csv'))
race_results = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'results.pkl'])))
race_info = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'race_info.pkl'])))
team_info = pd.read_pickle(os.path.join(base_path, os.sep.join(['pickles', 'team_info.pkl'])))

def calculate_entire_career_distance():
    # Filter race results for Fernando Alonso
    alonso_results = race_results[race_results['driverId'] == 'alonso']
    
    # Merge race results with race info to get the course length
    merged_data = alonso_results.merge(race_info, on='raceId')
    
    # Parse the date column as datetime
    merged_data['date'] = pd.to_datetime(merged_data['date'])
    
    # Calculate distance for each race
    merged_data['race_distance'] = merged_data['laps'] * merged_data['course_length_km']
    
    # Sum the distances to get the entire career distance driven
    total_distance = merged_data['race_distance'].sum()
    
    return total_distance, merged_data

def calculate_distance_per_team(merged_data):
    # Merge with team info to get the full team names
    merged_data = merged_data.merge(team_info[['teamId', 'team']], left_on='constructorId', right_on='teamId', how='left')
    
    # Group by team and sum the distances
    distance_per_team = merged_data.groupby('team')['race_distance'].sum().reset_index()
    
    # Merge with career summary to get start seasons for sorting
    team_start_seasons = career_summary.groupby('constructor')['startSeason'].min().reset_index()
    
    # Merge distance_per_team with team_start_seasons
    distance_per_team = distance_per_team.merge(team_start_seasons, left_on='team', right_on='constructor', how='left')
    
    # Sort by start season to ensure chronological order
    distance_per_team = distance_per_team.sort_values(by='startSeason').reset_index(drop=True)
    
    # Select relevant columns and rename them
    distance_per_team = distance_per_team[['team', 'race_distance']].rename(columns={'team': 'Team', 'race_distance': 'Total Distance (km)'})
    
    return distance_per_team

# Calculate the entire career distance and merged data
total_distance, merged_data = calculate_entire_career_distance()
print(f"Total distance driven by Fernando Alonso in his entire career: {total_distance:.2f} km")

# Calculate the distance per team
distance_per_team = calculate_distance_per_team(merged_data)

# Save the results
distance_per_team.to_csv(os.path.join(base_path, 'csv', 'distance_per_team.csv'), index=False)
distance_per_team.to_pickle(os.path.join(base_path, 'pickles', 'distance_per_team.pkl'))

# Display the results
print(distance_per_team)

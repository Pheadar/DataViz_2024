# creates career overview of a driver

import pandas as pd
import os
import json


# load data
base_path = os.path.join(os.curdir, 'treated_data')
results = pd.read_pickle(os.path.join(base_path, 'pickles', 'results.pkl'))
driver_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'driver_info.pkl'))
team_info = pd.read_pickle(os.path.join(base_path, 'pickles', 'team_info.pkl'))



def find_driver():
    # ask user for driver name or code
    driver_name = input("Enter driver name or code: ")

    # filter driver (find closest matches and ask user to select)
    # matches can be on driver name or code
    driver_matches = driver_info[
        driver_info['driverName'].str.contains(driver_name, case=False) |
        driver_info['driverCode'].str.contains(driver_name, case=False)
    ]
    
    if driver_matches.empty:
        print("No driver found. Try again.")
        return None
    elif len(driver_matches) == 1:
        return driver_matches.iloc[0]
    else:
        print("Multiple drivers found. Please select one:")
        index_list = list(driver_matches.index)  # Create a list of indices
        for idx, driver in enumerate(driver_matches.itertuples(), start=1):
            print(f"{idx}: {driver.driverName} ({driver.driverCode}), {driver.driverNationality}, born {driver.dob}")
        
        driver_choice = int(input("Enter driver number: ")) - 1  # Adjust for zero-based index
        if driver_choice < 0 or driver_choice >= len(index_list):
            print("Invalid selection. Please try again.")
            return None
        
        driver_index = index_list[driver_choice]  # Get the actual DataFrame index from the list
        return driver_matches.loc[driver_index]



def all_teams(driver_id, driver_code, driver_name):
    driver_results = results[results['driverId'] == driver_id]
    teams_data = []

    # For each team the driver has driven for
    for team in driver_results['constructorId'].unique():
        team_results = driver_results[driver_results['constructorId'] == team]
        team_name = team_info[team_info['teamId'] == team]['team'].values[0]
        seasons = sorted(team_results['season'].unique().astype(int))

        # Find separate stints within the same team
        stints = []
        previous_season = None
        stint_start = None

        for season in seasons:
            if previous_season is None or season == previous_season + 1:
                if stint_start is None:
                    stint_start = season
            else:
                stints.append((stint_start, previous_season))
                stint_start = season
            previous_season = season
        # Add last stint
        stints.append((stint_start, previous_season))

        # Append each stint data
        for stint in stints:
            min_season, max_season = stint
            total_seasons = max_season - min_season + 1
            teams_data.append({
                'driverCode': driver_code,
                'driverName': driver_name,
                'driverId': driver_id,
                'constructor': team_name,
                'startSeason': min_season,
                'endSeason': max_season,
                'totalSeasons': total_seasons
            })

    return teams_data

    

def driver_career():
    # Finds driver
    driver = find_driver()
    if driver is None:
        return "Driver not found or no selection made."
    
    # Extracts driver details
    driver_id = driver['driverId']
    driver_name = driver['driverName']
    driver_code = driver['driverCode']

    # Gets all team stints
    teams_data = all_teams(driver_id, driver_code, driver_name)

    # Compile the career overview
    career_overview = []
    for stint in teams_data:
        career_overview.append({
            'driverCode': driver_code,
            'driverName': driver_name,
            'driverId': driver_id,
            'constructor': stint['constructor'],
            'startSeason': stint['startSeason'],
            'endSeason': stint['endSeason'],
            'totalSeasons': stint['totalSeasons']
        })
    
    # Create DataFrame and sort it
    career_overview_df = pd.DataFrame(career_overview)
    career_overview_df = career_overview_df.sort_values(by='startSeason')  # Sorting by startSeason
    return career_overview_df



# save to csv
career_overview = driver_career()
if isinstance(career_overview, pd.DataFrame):
    driverId = career_overview['driverId'].iloc[0]
    csv_path = os.path.join(base_path, f"{driverId}_career_summary.csv")
    career_overview.to_csv(csv_path, index=False)
    print(f"Career overview saved to {csv_path}")
else:
    print(career_overview)
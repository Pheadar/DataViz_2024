# creates career overview of a driver

import pandas as pd
import os

driver_standings = pd.read_csv("treated_data/merged_driver_standings.csv")
driver_standings['Constructors'] = driver_standings['Constructors'].apply(lambda x: eval(x)[0]['constructorId'])

driver = input("Enter driver name or code: ").strip().upper()

def get_closest_matches(driver, driver_standings):
    from difflib import get_close_matches
    driver_standings['Driver.code'].fillna('Unknown', inplace=True)
    driver_standings['Driver.familyName'].fillna('Unknown', inplace=True)
    driver_standings['Driver.givenName'].fillna('Unknown', inplace=True)

    driver_codes = driver_standings['Driver.code'].astype(str).unique()
    driver_names = driver_standings['Driver.familyName'].astype(str).unique()
    driver_full_names = (driver_standings['Driver.givenName'] + " " + driver_standings['Driver.familyName']).unique()
    
    driver_full_names = [name.upper() for name in driver_full_names]
    driver_codes = [code.upper() for code in driver_codes]
    driver_names = [name.upper() for name in driver_names]

    matches = get_close_matches(driver, driver_codes + driver_names + driver_full_names, n=5, cutoff=0.6)
    return matches

matches = get_closest_matches(driver, driver_standings)
print("Possible matches (choose index):")

for i, match in enumerate(matches):
    filtered = driver_standings[driver_standings['Driver.code'].str.upper() == match]
    if not filtered.empty:
        driver_code = filtered['Driver.code'].values[0]
        driver_name = filtered['Driver.familyName'].values[0]
        print(f"{i}: {driver_code} - {driver_name}")
    else:
        print(f"{i}: {match} - No matching data found")

index = int(input("Choose the index of the driver you want: "))
driver = matches[index]

# filter data for driver
filter_cond = (driver_standings['Driver.code'].str.upper() == driver) | \
              (driver_standings['Driver.familyName'].str.upper() == driver) | \
              (driver_standings['Driver.givenName'].str.upper() == driver)
filtered_data = driver_standings[filter_cond]

if not filtered_data.empty:
    filtered_data = filtered_data[['Driver.code', 'season', 'Constructors', 'Driver.driverId']]

    i = 0
    if f"{driver}_data{i}.csv" in os.listdir("dataframes/"):
        while f"{driver}_career{i}.csv" in os.listdir("dataframes/"):
            i += 1
    filtered_data.to_csv(f"dataframes/{driver}_career{i}.csv", index=False)
    print(f"Data saved to dataframes/{driver}_career{i}.csv")

else:
    print("No data found to save.")
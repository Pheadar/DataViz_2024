
import pandas as pd

driver = input("Enter driver code: ").strip().upper()
while len(driver) > 3:
    driver = input("Enter driver code: ").strip().upper()

driver_standings = pd.read_csv("treated_data/merged_driver_standings.csv")
driver_standings = driver_standings[driver_standings['Driver.code'] == driver]
driver_standings['Constructors'] = driver_standings['Constructors'].apply(lambda x: eval(x)[0]['constructorId'])
driver_standings = driver_standings[['Driver.code', 'season', 'Constructors', 'Driver.driverId']]

driver_standings.to_csv(f"treated_data/{driver}_data.csv", index=False)
print(f"Data saved to treated_data/{driver}_data.csv")
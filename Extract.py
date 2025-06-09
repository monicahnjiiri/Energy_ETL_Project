import pandas as pd
import os

def extract_data():
    url = "https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv"
    df = pd.read_csv(url)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/energy_raw.csv", index=False)
    return df

if __name__ == "__main__":
    df = extract_data()
    print("✔ Data saved to data/raw/energy_raw.csv")
    print("✔ Rows:", df.shape[0], "Columns:", df.shape[1])

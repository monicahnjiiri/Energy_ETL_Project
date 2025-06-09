import pandas as pd
import os

def transform_data():
    df = pd.read_csv("data/raw/energy_raw.csv")
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])

    # Select Germany columns only
    de_cols = [col for col in df.columns if col.startswith("DE_")]
    de_df = df[["utc_timestamp"] + de_cols].copy()

    # Drop columns with >50% missing
    threshold = len(de_df) * 0.5
    de_df.dropna(axis=1, thresh=threshold, inplace=True)

    # Fill numeric columns with mean
    for col in de_df.columns:
        if de_df[col].isnull().any():
            if de_df[col].dtype == "object":
                de_df[col].fillna("Unknown", inplace=True)
            else:
                de_df[col].fillna(de_df[col].mean(), inplace=True)

    # Rename timestamp column
    de_df.rename(columns={"utc_timestamp": "timestamp"}, inplace=True)

    # Split: load vs generation
    load_cols = ["timestamp"] + [col for col in de_df.columns if "load" in col]
    gen_cols = ["timestamp"] + [col for col in de_df.columns if "generation" in col]

    load_df = de_df[load_cols]
    gen_df = de_df[gen_cols]

    # Save both cleaned CSVs
    os.makedirs("data/processed", exist_ok=True)
    load_df.to_csv("data/processed/germany_load.csv", index=False)
    gen_df.to_csv("data/processed/germany_generation.csv", index=False)

    return load_df, gen_df

if __name__ == "__main__":
    load_df, gen_df = transform_data()
    print("✔ Cleaned load saved: data/processed/germany_load.csv →", load_df.shape)
    print("✔ Cleaned generation saved: data/processed/germany_generation.csv →", gen_df.shape)

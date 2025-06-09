import os
import pymysql
import pandas as pd
from dotenv import load_dotenv

# Load env vars
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def connect():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True
    )

def create_table_from_csv(cursor, df, table_name):
    columns = []
    for col in df.columns:
        if "time" in col.lower():
            columns.append(f"`{col}` DATETIME")
        else:
            columns.append(f"`{col}` FLOAT")
    column_defs = ", ".join(columns)
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
    cursor.execute(f"CREATE TABLE `{table_name}` ({column_defs})")

def insert_data(cursor, df, table_name):
    cols = ", ".join([f"`{col}`" for col in df.columns])
    placeholders = ", ".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders})"
    data = [tuple(row) for _, row in df.iterrows()]
    cursor.executemany(sql, data)

def load_data():
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                for file_name, table_name in [
                    ("data/processed/germany_load.csv", "germany_load"),
                    ("data/processed/germany_generation.csv", "germany_generation")
                ]:
                    df = pd.read_csv(file_name)
                    create_table_from_csv(cursor, df, table_name)
                    insert_data(cursor, df, table_name)
                    print(f"✔ Loaded into `{table_name}` ({len(df)} rows)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    load_data()



import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load .env file
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "earthquake_db")

# CSV path in project root
# Path to CSV file
CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "earthquakes_5years_full_schema.csv"
)


# Create database engine
uri = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(uri, echo=False, pool_pre_ping=True)

def main():
    print("Using DB:", DB_NAME, "as user:", DB_USER)
    print("Reading CSV:", CSV_PATH)

    df = pd.read_csv(CSV_PATH, parse_dates=["time"])
    print("Rows in CSV:", len(df))

    print("Writing to MySQL table 'earthquakes'...")
    df.to_sql("earthquakes", con=engine, if_exists="replace", index=False, chunksize=1000)
    print("Done! Data loaded successfully.")

if __name__ == "__main__":
    main()

import requests
import duckdb
import time
from tabulate import tabulate
from datetime import datetime

# List of endpoints
ENDPOINTS = [
    "http://192.168.100.101/api/system/info",
    "http://192.168.100.102/api/system/info",
    "http://192.168.100.103/api/system/info",
    "http://192.168.100.104/api/system/info"
]

# DuckDB setup
DB_NAME = "miner_stats.duckdb"
TABLE_NAME = "stats"

# Initialize database and table
con = duckdb.connect(DB_NAME)
con.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    timestamp TIMESTAMP,
    hostname TEXT,
    temp FLOAT,
    vrTemp FLOAT,
    hashRate INT,
    bestSessionDiff TEXT,
    stratumDiff INT
);
""")

def fetch_data(endpoint):
    try:
        response = requests.get(endpoint, timeout=5)
        data = response.json()
        return {
            "hostname": data.get("hostname"),
            "temp": data.get("temp"),
            "vrTemp": data.get("vrTemp"),
            "hashRate": int(data.get("hashRate", 0)),  # truncate decimals
            "bestSessionDiff": data.get("bestSessionDiff"),
            "stratumDiff": data.get("stratumDiff")
        }
    except Exception as e:
        print(f"Failed to fetch data from {endpoint}: {e}")
        return None

def store_data(con, row):
    con.execute(f"""
        INSERT INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now(), row["hostname"], row["temp"], row["vrTemp"],
          row["hashRate"], row["bestSessionDiff"], row["stratumDiff"]))

def display_matrix(con):
    rows = con.execute(f"""
        SELECT hostname, temp, vrTemp, hashRate, bestSessionDiff, stratumDiff
        FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY hostname ORDER BY timestamp DESC) as rn
            FROM {TABLE_NAME}
        ) WHERE rn = 1
    """).fetchall()

    headers = ["Hostname", "Temp", "vrTemp", "HashRate", "BestSessionDiff", "StratumDiff"]
    print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))

def main_loop():
    while True:
        print(f"\n[INFO] Polling at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        for endpoint in ENDPOINTS:
            data = fetch_data(endpoint)
            if data:
                store_data(con, data)
        display_matrix(con)
        time.sleep(180)  # Wait for 3 minutes

if __name__ == "__main__":
    main_loop()

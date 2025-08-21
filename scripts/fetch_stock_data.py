import os
import requests
import psycopg2
from psycopg2.extras import execute_values

def fetch_and_store():
    api_key = os.getenv('API_KEY')
    postgres_url = os.getenv('POSTGRES_URL')
    symbol = os.getenv('STOCK_SYMBOL', 'IBM')  # use env variable or default stock

    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '60min',
        'apikey': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Error check for API limit or missing data
        if 'Time Series (60min)' not in data:
            raise ValueError("No stock data found in API response.")

        time_series = data['Time Series (60min)']
        rows = []
        for timestamp, stats in time_series.items():
            rows.append((
                symbol,
                timestamp,
                float(stats['1. open']),
                float(stats['2. high']),
                float(stats['3. low']),
                float(stats['4. close']),
                int(float(stats['5. volume']))
            ))

        with psycopg2.connect(postgres_url) as conn:
            with conn.cursor() as cur:
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS stock_prices (
                  symbol VARCHAR(10),
                  timestamp TIMESTAMP,
                  open FLOAT, high FLOAT, low FLOAT,
                  close FLOAT, volume BIGINT,
                  PRIMARY KEY (symbol, timestamp)
                );
                """
                cur.execute(create_table_sql)
                upsert_sql = """
                INSERT INTO stock_prices (symbol, timestamp, open, high, low, close, volume)
                VALUES %s
                ON CONFLICT (symbol, timestamp) DO UPDATE
                    SET open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume;
                """
                execute_values(cur, upsert_sql, rows)

        print(f"Inserted/updated {len(rows)} rows.")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    fetch_and_store()

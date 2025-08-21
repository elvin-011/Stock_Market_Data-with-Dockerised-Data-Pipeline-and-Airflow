###### Stock Market Data Pipeline with Dockerized Airflow & PostgreSQL

This project is a data pipeline to fetch stock market data using the Alpha Vantage API, process and store it in a PostgreSQL database, orchestrated by Apache Airflow running in Docker containers.

***

###Features

- Fetches intraday stock data hourly via Alpha Vantage API
- Stores stock price data in PostgreSQL with upsert functionality
- Pipeline managed and scheduled with Apache Airflow
- Fully containerized setup using Docker and Docker Compose
- Easy deployment and extensibility

### Prerequisites**

Make sure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- (Optional) PostgreSQL Client or GUI tool such as [DBeaver](https://dbeaver.io/), [pgAdmin](https://www.pgadmin.org/), or [psql](https://www.postgresql.org/docs/current/app-psql.html)
-
##### Getting Started
### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/stock-market-pipeline.git
cd stock-market-pipeline
```

### 2. Configure Environment Variables

Remove the .example from the .env.example file and update the info in the env file with your data

- **API_KEY:** Get yours free from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
- **FERNET_KEY:** Generate with Python:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

- **AIRFLOW__WEBSERVER__SECRET_KEY:** Generate with Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

***

###3. Start Docker Containers

Run the following to build and start Airflow, PostgreSQL, and dependencies:

```bash
docker-compose up -d
```

- This sets up:
  - PostgreSQL database on port 5432
  - Airflow webserver on port 8080
  - Airflow scheduler and executor in containers

***

### 4. Access Airflow UI

Open your browser and go to:

```
http://localhost:8080
```

- Create an Airflow admin user if authentication is enabled (use `docker-compose run airflow-webserver airflow users create --username "ANY NAME" --firstname "FIRSTNAME" --lastname "LASTNAME" --role Admin --email "EMAIL_ID" --password "ANY PASSWORD"`)
- Enable the `stock_data_pipeline` DAG by toggling it ON.
- Trigger a manual run or wait for the schedule trigger (hourly).

***

### 5. Verify Data in PostgreSQL

Access your database to verify stock data:

```bash
docker-compose exec postgres psql -U airflow -d airflow_db
```

Run SQL query:

```sql
SELECT * FROM stock_prices LIMIT 10;
```

You should see the latest stock prices.

***

## Project Structure

```
├── dags/                  # Airflow DAG definitions
│   └── stock_data_dag.py
├── scripts/               # Stock data fetching and insertion script
│   └── fetch_stock_data.py
├── docker-compose.yml     # Docker Compose configuration
├── .env                   # Environment variables (not in repo)
├── requirements.txt       # Python dependencies (for extension)
└── README.md              # This file
```

***

## Troubleshooting

- **Airflow UI not accessible:**  
  - Confirm Docker containers are running (`docker-compose ps`)  
  - Verify ports 8080 (Airflow) and 5432 (Postgres) are open  
  - Check Airflow webserver logs via `docker-compose logs airflow-webserver`

- **Database connection/authentication issues:**  
  - Confirm `.env` passwords match between Postgres and Airflow  
  - Reset passwords in PostgreSQL container if needed  
  - Verify `POSTGRES_URL` is consistent with credentials

- **DAG task fails:**  
  - Check task logs in Airflow UI  
  - Verify your scripts folder is mounted correctly in Docker containers  
  - Ensure API Key is valid and quota limits not exceeded

***

## Extending the Pipeline

- Change the `STOCK_SYMBOL` in `.env` to fetch different stock data
- Add more DAGs or tasks for data processing/analytics
- Integrate other data sources or visualization tools

***

## License

This project is licensed under the MIT License.

***

For any issues or feature requests, please open an issue or contact the maintainer.

***

This README provides users with all needed steps and info to run your system locally after cloning from GitHub. Let me know if you want me to generate it as a downloadable file for you!




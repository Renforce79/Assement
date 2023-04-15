#!/bin/bash

set -e

# Start the PostgreSQL service
service postgresql start

# Change password for user postgres
su postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres';\""

# Initialize the Airflow database
airflow db init

# Start the Airflow web server and scheduler
airflow webserver -D &
airflow scheduler -D &

# Wait for the Airflow web server and scheduler to start
echo "Waiting for Airflow web server and scheduler to start..."
sleep 30

# Trigger the Airflow DAG with the specified file path
airflow dags trigger ejecutar_miproyecto -r ejecutar_miproyecto --conf '{"file_path":"/code/BING_MultiDays.csv"}'

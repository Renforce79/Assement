#!/bin/bash

set -e

# Start the PostgreSQL service
service postgresql start

# Change password for user postgres
su postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres';\""

# Initialize the Airflow database
airflow db init

# Start the Airflow web server
airflow webserver -p 3000 -D

# Wait for the Airflow web server to start
echo "Waiting for Airflow web server to start..."
while true; do
    _RUNNING=$(ps aux | grep airflow-webserver | grep -v grep)
    if [ -z "${_RUNNING}" ]; then
        sleep 1
    else
        break
    fi
done

# Start the Airflow scheduler
airflow scheduler -D

# Wait for the Airflow scheduler to start
echo "Waiting for Airflow scheduler to start..."
while true; do
    _RUNNING=$(ps aux | grep airflow-scheduler | grep -v grep)
    if [ -z "${_RUNNING}" ]; then
        sleep 1
    else
        break
    fi
done

# Trigger the Airflow DAG with the specified file path
airflow dags trigger ejecutar_miproyecto

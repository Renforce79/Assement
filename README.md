## Loading layouts, with Python and Docker.
## Configuration for local execution


## Library installation

The following commands are necessary to install the project's dependent libraries.

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
service postgresql status
sudo service postgresql start
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"

pip install apache-airflow

```

## Local Execution

airflow db init
airflow webserver -p 8080
airflow scheduler 

# Trigger the Airflow DAG with the specified file path
airflow dags trigger ejecutar_miproyecto


## Execute API from container

1. Build image
```bash
sudo docker build -t parsing-data . 
```

2. Create container
```bash
sudo docker run --name load-parsing-data -p 8080:8080 parsing-data
```

3. Check real-time logs
```bash
sudo docker logs -f parsing-data
```

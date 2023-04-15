FROM python:3.8-slim-buster

# Install sudo
RUN apt-get update && apt-get install -y sudo

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

RUN pip install psycopg2-binary

# Install PostgreSQL and other dependencies
RUN apt-get install -y --no-install-recommends \
    gnupg2 \
    libffi6 \
    libpq-dev \
    libssl-dev \
    postgresql \
    postgresql-client \
    python3-dev \
    python3-pip \
    python3-venv \
    && pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir apache-airflow[crypto,postgres] \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN service postgresql start && service postgresql status

# Start the PostgreSQL service and change password for user postgres
RUN service postgresql start && su postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres';\""

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./BING_MultiDays.csv /code/BING_MultiDays.csv
COPY ./load_data.py /code/load_data.py
COPY ./load_data_DAG.py /code/load_data_DAG.py
COPY ./entrypoint.sh /code/entrypoint.sh

RUN pip install markupsafe==1.1.1

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Set the executable flag on the entrypoint script
RUN chmod +x /code/entrypoint.sh

# Set the entrypoint script to run on container startup
ENTRYPOINT ["/code/entrypoint.sh"]


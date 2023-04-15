import pandas as pd
import psycopg2
import csv
from datetime import datetime as dt


# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres",
    port=5433
)

cursor = conn.cursor()

# Create the tables
create_customer_table = """
CREATE TABLE IF NOT EXISTS customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255),
    account_number VARCHAR(255),
    account_name VARCHAR(255),
    account_status VARCHAR(255)
);
"""

create_campaign_table = """
CREATE TABLE IF NOT EXISTS campaign (
    campaign_id INT PRIMARY KEY,
    campaign_name VARCHAR(255),
    campaign_status VARCHAR(255),
    customer_id INT REFERENCES customer(customer_id)
);
"""

create_ad_group_table = """
CREATE TABLE IF NOT EXISTS ad_groups (
    ad_group_id INT PRIMARY KEY,
    ad_group_name VARCHAR(255),
    ad_group_status VARCHAR(255),
    campaign_id INT REFERENCES campaign(campaign_id)
);
"""

create_ad_table = """
CREATE TABLE ads (
ad_id SERIAL PRIMARY KEY,
ad_description TEXT,
ad_distribution TEXT,
ad_status TEXT,
ad_title TEXT,
ad_type TEXT,
tracking_template TEXT,
custom_parameters TEXT,
final_mobile_url TEXT,
final_url TEXT,
top_vs_other TEXT,
display_url TEXT,
final_app_url TEXT,
destination_url TEXT,
ad_group_id INT REFERENCES ad_groups(ad_group_id)
);
"""

create_impressions_table = """
CREATE TABLE impressions (
impression_id SERIAL PRIMARY KEY,
impression_date DATE,
device_type TEXT,
device_os TEXT,
delivered_match_type TEXT,
bid_match_type TEXT,
language TEXT,
network TEXT,
currency_code TEXT,
impressions INTEGER,
clicks INTEGER,
spend NUMERIC,
avg_position NUMERIC,
conversions INTEGER,
assists INTEGER,
ad_id INTEGER REFERENCES ads(ad_id)
);
"""

cursor.execute(create_customer_table)
cursor.execute(create_campaign_table)
cursor.execute(create_ad_group_table)
cursor.execute(create_ad_table)
cursor.execute(create_impressions_table)

conn.commit()
cursor.close()
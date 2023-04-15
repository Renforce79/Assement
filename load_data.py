import pandas as pd
import psycopg2
import csv
from datetime import datetime as dt
import os
dag_folder = os.path.dirname(os.path.abspath(__file__))

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres",
    port=5433
)

cursor = conn.cursor()

# Create a sequence to generate IDs for the customers
cursor.execute("CREATE SEQUENCE IF NOT EXISTS customer_id_seq")
cursor.execute("CREATE SEQUENCE IF NOT EXISTS campaign_id_seq")
cursor.execute("CREATE SEQUENCE IF NOT EXISTS ad_group_id_seq")

# Load the CSV file into a pandas dataframe

df = pd.read_csv('{}/BING_MultiDays.csv'.format(dag_folder), skiprows=9)

# Remove the last 12509 or more rows
df = df.iloc[:-2]

# Save the filtered dataframe to a new CSV file
df.to_csv('{}/filtered_BING_MultiDays.csv'.format(dag_folder), index=False)


with open('{}/filtered_BING_MultiDays.csv'.format(dag_folder), 'rb') as file:
    csv_reader = csv.reader(file, delimiter=',')
    headers = next(csv_reader)

# Open the CSV file and insert its contents into the customer table
with open('{}/filtered_BING_MultiDays.csv'.format(dag_folder), 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Generate a new ID for the customer using the sequence
        cursor.execute("SELECT nextval('customer_id_seq')")
        customer_id = cursor.fetchone()[0]
        customer_name = row["Customer"]
        account_number = row["Account number"]
        account_name = row["Account name"]
        account_status = row["Account status"]

        # Insert the row into the "customer" table
        insert_customer = """INSERT INTO customer (customer_id, customer_name, account_number, account_name, account_status) VALUES ('{}','{}', '{}', '{}', '{}')""".format(customer_id, customer_name,account_number,account_name,account_status)
 
        cursor.execute(insert_customer)
        
        # Generate a new ID for the campaign using the sequence
        cursor.execute("SELECT nextval('campaign_id_seq')")
        campaign_id = cursor.fetchone()[0]
        campaign_name = row["Campaign name"]
        campaign_status = row["Campaign status"]
        
        # Insert the row into the "campaign" table
        insert_campaign = """INSERT INTO campaign (campaign_id, campaign_name, campaign_status, customer_id) VALUES ('{}', '{}', '{}', '{}')""".format(campaign_id, campaign_name, campaign_status, customer_id)
        cursor.execute(insert_campaign)

        # Generate a new ID for the ad_group using the sequence
        cursor.execute("SELECT nextval('ad_group_id_seq')")
        ad_group_id = cursor.fetchone()[0]
        ad_group_name = row["Ad group"]
        ad_group_status = row["Ad group status"]
        
        # Insert the row into the "ad_groups" table
        insert_ad_group = """INSERT INTO ad_groups (ad_group_id, ad_group_name, ad_group_status, campaign_id) VALUES ('{}', '{}', '{}', '{}')""".format(ad_group_id, ad_group_name, ad_group_status, campaign_id)
        cursor.execute(insert_ad_group)

        
        # Insert the ads and impressions associated with the ad group
        ad_description = row["Ad description"]
        ad_description = ad_description.replace("'", "''") # Replace single quotes with double single quotes
        ad_distribution = row["Ad distribution"]
        ad_status = row["Ad status"]
        ad_title = row["Ad title"]
        ad_type = row["Ad type"]
        tracking_template = row["Tracking Template"]
        custom_parameters = row["Custom Parameters"]
        final_mobile_url = row["Final Mobile URL"]
        final_url = row["Final URL"]
        top_vs_other = row["Top vs. other"]
        display_url = row["Display URL"]
        final_app_url = row["Final App URL"]
        destination_url = row["Destination URL"]
        
        # Insert the row into the "ads" table
        insert_ad = """INSERT INTO ads (ad_description, ad_distribution, ad_status, ad_title, ad_type, tracking_template, custom_parameters, final_mobile_url, final_url, top_vs_other, display_url, final_app_url, destination_url, ad_group_id) 
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') RETURNING ad_id;""".format(ad_description, ad_distribution, ad_status, ad_title, ad_type, tracking_template, custom_parameters, final_mobile_url, final_url, top_vs_other, display_url, final_app_url, destination_url, ad_group_id)
        
        cursor.execute(insert_ad)
        ad_id = cursor.fetchone()[0]
        
        # Check if the date column is null and handle accordingly
        try:
            impression_date = dt.strptime(row["Gregorian date"], '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            impression_date = dt.strptime(row["Gregorian date"], '%Y-%m-%d').strftime('%Y-%m-%d')
        device_type = row["Device type"]
        device_os = row["Device OS"]
        delivered_match_type = row["Delivered match type"]
        bid_match_type = row["BidMatchType"]
        language = row["Language"]
        network = row["Network"]
        currency_code = row["Currency code"]
        impressions = row["Impressions"] if row["Impressions"] else 0
        clicks = row["Clicks"] if row["Clicks"] else 0
        spend = row["Spend"] if row["Spend"] else 0
        avg_position = row["Avg. position"] if row["Avg. position"] else 0
        conversions = row["Conversions"] if row["Conversions"] else 0
        assists = row["Assists"] if row["Assists"] else 0
        
        # Insert the row into the "impressions" table
        insert_impression = """INSERT INTO impressions (impression_date, device_type, device_os, delivered_match_type, bid_match_type, language, network, currency_code, impressions, clicks, spend, avg_position, conversions, assists, ad_id) 
                                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, '{}')""".format(impression_date, device_type, device_os, delivered_match_type, bid_match_type, language, network, currency_code, impressions, clicks, spend, avg_position, conversions, assists, ad_id)
        
        cursor.execute(insert_impression)

# Commit the changes to the database and close the cursor and connection
conn.commit()
cursor.close()
conn.close()

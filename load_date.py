#!/usr/bin/env python3

DATA_FILE='Crowd-Sourced_Price_Collection_CSV.csv'
DB_NAME='csi4142'
DB_USER='csi4142'
DB_HOST='localhost'
DB_PASS=''

import csv, datetime, psycopg2

# Connect to the PostgreSQL database with the provided info.
def connect_db(dbname, user, host, password):
    print("Connecting to database")
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
    print("Connected to database")
    return conn

# Loads the data from the main dataset into memory as a set of tuples.
def load_data_from_file(f):
    print("Loading data from file")
    reader = csv.DictReader(f)

    data = [(
            row['Line'],
            row['Country'],
            row['Location Code'],
            row['Location Name'],
            row['Outlet Code'],
            row['Outlet Type'],
            row['Obs Date (yyyy-MM-dd)'],
            row['Product Code'],
            row['Product Name'],
            row['Pref. Qty'],
            row['Obs. Qty'],
            row['Quantity'],
            row['Obs. UoM Code'],
            row['Obs Price'],
            row['Conv. Price'],
            row['Price Type Name'],
            row['Rejected'],
            row['Currency'],
        ) for row in reader]

    return data

# Converts an individual date from the original format to the expected format.
def parse_date(date):
    from datetime import datetime

    # Convert the date from a string to a python `Date` object.
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    # Get the required date attributes.
    day_of_week = date_obj.weekday()
    result = {
        "date": date_obj,
        "day_of_week": day_of_week,
        "week_in_year": date_obj.isocalendar()[1],
        "month": date_obj.month,
        "year": date_obj.year,
        # The datetime module classifies Mon-Fri as days 0-4, with Saturday and
        # Sunday being days 5 and 6.
        "weekend": day_of_week >= 5,
    }

    return result

if __name__ == '__main__':
    # Connect to the PostgreSQL database.
    conn = connect_db(DB_NAME, DB_USER, DB_HOST, DB_PASS)

    # Open the CSV file with the main dataset and read it into memory as a set
    # of tuples.
    with open(DATA_FILE, 'r') as f:
        data = load_data_from_file(f)

    # Filter the data down to just the dates.
    dates = [entry[6] for entry in data]

    # Ensure there are no duplicate dates in the list.
    dates = set(dates)

    # Parse the dates into the expected format.
    print("Parsing dates to proper format")
    dates = [parse_date(date) for date in dates]

    # Execute the query to insert the data.
    print("Executing query")
    cur = conn.cursor()
    query = """
INSERT INTO csi4142project.Date (date, day_of_week, week_in_year, month, year, weekend) VALUES (%(date)s, %(day_of_week)s, %(week_in_year)s, %(month)s, %(year)s, %(weekend)s)
"""
    cur.executemany(query, dates)
    conn.commit()

    # Close the database connection
    conn.close()

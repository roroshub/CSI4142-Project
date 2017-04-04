#!/usr/bin/env python3

import datetime
import sys
import time

# In this example, we use psycopg2. You can change it to another driver,
# but then the method pgcopybulkloader won't work as we use driver-specific
# code there.
# You can make another function or declare facttbl (see further below) to
# be a BatchFactTable such that you don't need special
# bulk loading methods.

import psycopg2

# Depending on your system, you might have to do something like this
# where you append the path where pygrametl is installed
# NOTE: uncomment this if necessary
#sys.path.append('/home/me/code')

import pygrametl
from pygrametl.datasources import CSVSource, MergeJoiningSource, SQLSource
from pygrametl.tables import CachedDimension, SnowflakedDimension,\
    SlowlyChangingDimension, BulkFactTable


# This controls the behaviour of the script.
# If the script is in debug mode, it will only insert the specified number of
# rows into the database from the original data set (to speed up the development
# process).
DEBUG=True
ROWS_TO_IMPORT=10

DATA_FILE='Crowd-Sourced_Price_Collection_CSV.csv'
DB_NAME='csi4142'
DB_USER='csi4142'
DB_HOST='localhost'
DB_PASS=''


# Connection to the target data warehouse:
pgconn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
        password=DB_PASS)
connection = pygrametl.ConnectionWrapper(pgconn)
connection.setasdefault()
connection.execute('set search_path to csi4142project')


# Methods
def pgcopybulkloader(name, atts, fieldsep, rowsep, nullval, filehandle):
    # Here we use driver-specific code to get fast bulk loading.
    # You can change this method if you use another driver or you can
    # use the FactTable or BatchFactTable classes (which don't require
    # use of driver-specifc code) instead of the BulkFactTable class.
    global connection
    curs = connection.cursor()
    curs.copy_from(file=filehandle, table=name, sep=fieldsep,
                   null=str(nullval), columns=atts)

def locationhandling(row, namemapping):
    from datetime import datetime

    date = pygrametl.getvalue(row, 'date', namemapping)
    # Convert the date from a string to a python `Date` object.
    date = datetime.strptime(date, '%Y-%m-%d').date()
    row['location_year'] = date.year
    return row

# Data dimensions

locationdim = CachedDimension(
    name='Location',
    key='location_key',
    attributes=['city', 'country', 'location_year'],
    lookupatts=['location_key'],
    rowexpander=locationhandling)

productdim = CachedDimension(
    name='Product',
    key='product_key',
    attributes=['product_name'],
    lookupatts=['product_key'])

datedim = CachedDimension(
    name='Date',
    key='date_key',
    attributes=['date', 'day_of_week', 'week_in_year', 'month', 'year', 'weekend'],
    lookupatts=['date'])

facttbl = BulkFactTable(
    name='ProductPrice',
    keyrefs=['date_key', 'pp_key', 'product_key', 'location_key'],
    measures=['price'], # TODO: determine if any other measures should be listed
    bulkloader=pgcopybulkloader,
    bulksize=5000000,
    nullsubst='N/A') # TODO: replace this with a better NULL substitution value

# Data sources

# The buffer size is set to 16384 B, because this performs best, according to
# the pygrametl developers.
data_set = CSVSource(open(DATA_FILE, 'r', 16384),
                        delimiter=',')

def main():
    #[datedim.insert(row) for row in date_source]
    count = 1
    for row in data_set:
        # Add the missing data to the dimension tables.
        row['date_key'] = datedim.lookup(row, { 'date': 'Obs Date (yyyy-MM-dd)' })
        row['price'] = row['Obs Price']
        row['pp_key'] = count # FIXME
        row['product_key'] = productdim.ensure(row, {
            'product_key': 'Product Code',
            'product_name': 'Product Name' })
        row['location_key'] = locationdim.ensure(row, {
            'location_key': 'Location Code',
            'city': 'Location Name',
            'country': 'Country',
            'date': 'Obs Date (yyyy-MM-dd)' })

        # Insert the data into the fact table.
        facttbl.insert(row)

        count += 1

        # If in debug mode, only insert the specified number of rows into the
        # database.
        if DEBUG and count > ROWS_TO_IMPORT:
            break
    connection.commit()

if __name__ == '__main__':
    main()

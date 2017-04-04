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
from pygrametl.datasources import CSVSource, HashJoiningSource, SQLSource
from pygrametl.tables import CachedDimension, SnowflakedDimension,\
    SlowlyChangingDimension, BulkFactTable


# This controls the behaviour of the script.
# If the script is in debug mode, it will only insert the specified number of
# rows into the database from the original data set (to speed up the development
# process).
DEBUG=True
ROWS_TO_IMPORT=10

DATA_FILE='Crowd-Sourced_Price_Collection_CSV.csv'
GDP_FILE='API_NY.GDP.MKTP.CD_DS2_en_csv_v2.csv'
POPULATION_FILE='API_SP.POP.TOTL_DS2_en_csv_v2.csv'
LIFE_EXPECTANCY_FILE='API_SP.DYN.LE00.IN_DS2_en_csv_v2.csv'
GNI_FILE='API_NY.GNP.PCAP.CD_DS2_en_csv_v2.csv'
NUTRITION_FILE='nutrition.csv'
DB_NAME='csi4142'
DB_USER='csi4142'
DB_HOST='localhost'
DB_PASS=''

# Global variables used for in-memory stores.
POP_DATA = {}
LIFE_EXPECTANCY_DATA = {}
GNI_DATA = {}
NUTRITION_DATA = {}


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

def load_pop_data_set(data):
    # Load the population dataset into memory as a dictionary.
    # Hard-coded to only load 2012 data.
    dataset = {}
    for row in data:
        dataset[row['\ufeff"Country Name"']] = row['2012']

    return dataset

def load_life_expectancy_data_set(data):
    # Load the life expectancy dataset into memory as a dictionary.
    # Hard-coded to only load 2012 data.
    dataset = {}
    for row in data:
        dataset[row['\ufeff"Country Name"']] = row['2012']

    return dataset

def load_gni_data_set(data):
    # Load the GNI dataset into memory as a dictionary.
    # Hard-coded to only load 2012 data.
    dataset = {}
    for row in data:
        dataset[row['\ufeff"Country Name"']] = row['2012']

    return dataset

def load_nutrition_data_set(data):
    # Load the nutrition dataset into memory as a dictionary.
    dataset = {}
    for row in data:
        dataset[row['product_name']] = row

    return dataset

def producthandling(row, namemapping):
    from datetime import datetime

    date = pygrametl.getvalue(row, 'date', namemapping)
    # Convert the date from a string to a python `Date` object.
    date = datetime.strptime(date, '%Y-%m-%d').date()
    row['product_year'] = date.year

    product_name = pygrametl.getvalue(row, 'product_name', namemapping)
    # Set the nutrition values
    if product_name in NUTRITION_DATA:
        product = NUTRITION_DATA[product_name]
        row['category'] = product['category']
        row['energy'] = product['energy']
        row['carbohydrates'] = product['carbohydrates']
        row['fat'] = product['fat']
        row['protein'] = product['protein']
    else:
        row['category'] = None
        row['energy'] = None
        row['carbohydrates'] = None
        row['fat'] = None
        row['protein'] = None

    return row

def locationhandling(row, namemapping):
    from datetime import datetime

    country = row['Country']

    # Set the population value
    if country in POP_DATA:
        row['population'] = POP_DATA[country]
    else:
        row['population'] = None

    # Set the life expectancy value
    if country in LIFE_EXPECTANCY_DATA:
        row['life_expectancy'] = LIFE_EXPECTANCY_DATA[country]
    else:
        row['life_expectancy'] = None

    # Set the annual average income value
    if country in GNI_DATA:
        row['anav_income'] = GNI_DATA[country]
    else:
        row['anav_income'] = None

    date = pygrametl.getvalue(row, 'date', namemapping)
    # Convert the date from a string to a python `Date` object.
    date = datetime.strptime(date, '%Y-%m-%d').date()
    row['location_year'] = date.year

    # The year for which to retrieve the GDP is hard-coded to simplify the ETL
    # process, and because the data only covers 2012.
    row['gdp'] = pygrametl.getvalue(row, '2012', namemapping)

    return row

# Data dimensions

locationdim = CachedDimension(
    name='Location',
    key='location_key',
    attributes=['city', 'country', 'gdp', 'population', 'life_expectancy',
        'anav_income', 'location_year'],
    lookupatts=['location_key'],
    rowexpander=locationhandling)

productdim = CachedDimension(
    name='Product',
    key='product_key',
    attributes=['product_name', 'category', 'energy', 'carbohydrates', 'fat',
        'protein', 'product_year'],
    lookupatts=['product_key'],
    rowexpander=producthandling)

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

gdp_data_set = CSVSource(open(GDP_FILE, 'r', 16384),
                        delimiter=',')
pop_data_set = CSVSource(open(POPULATION_FILE, 'r', 16384),
                        delimiter=',')
life_expectancy_data_set = CSVSource(open(LIFE_EXPECTANCY_FILE, 'r', 16384),
                        delimiter=',')
gni_data_set = CSVSource(open(GNI_FILE, 'r', 16384),
                        delimiter=',')
nutrition_data_set = CSVSource(open(NUTRITION_FILE, 'r', 16384),
                        delimiter=',')

data = HashJoiningSource(src1=data_set,
                         src2=gdp_data_set,
                         key1='Country',
                         key2='\ufeff"Country Name"')

POP_DATA = load_pop_data_set(pop_data_set)
LIFE_EXPECTANCY_DATA = load_life_expectancy_data_set(life_expectancy_data_set)
GNI_DATA = load_gni_data_set(gni_data_set)
NUTRITION_DATA = load_nutrition_data_set(nutrition_data_set)

def main():
    # Measure the time taken to perform the ETL process.
    start = time.time()

    count = 1
    for row in data:
        # Add the missing data to the dimension tables.
        row['date_key'] = datedim.lookup(row, { 'date': 'Obs Date (yyyy-MM-dd)' })
        row['price'] = row['Obs Price']
        row['pp_key'] = count # FIXME
        row['product_key'] = productdim.ensure(row, {
            'product_key': 'Product Code',
            'product_name': 'Product Name',
            'date': 'Obs Date (yyyy-MM-dd)' })
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

    end = time.time()
    print("ETL operation completed in: {}".format(end - start))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import csv, re

#DATA_FILE='Crowd-Sourced_Price_Collection_CSV.csv'
#OUT_FILE='Kenya_data.csv'
DATA_FILE='location-kenya.csv'
OUT_FILE='location-kenya_formatted.csv'
# If this value is set to an integer, the resulting data will only be output for
# the outlet code corresponding to this integer.
OUTLET_CODE=1748

# Loads the data from the main dataset into memory.
# def load_data_from_file(f):
#     # Read the file into memory as a list of lines
#     data = f.readlines()
# 
#     reader = csv.DictReader(f)
# 
#     dataset = []
#     for row in reader:
#         # Strip the loading and trailing characters inserted by PostgreSQL.
#         row = row[]
#         # Ignore non-Kenya rows
#         if row['Country'] != 'Kenya':
#             continue
# 
#         # Strip out the commas from the product names, as they interfere with
#         # the operation of the Apriori algorithm implemenation used.
#         product_name = row['Product Name'].replace(',', '')
# 
#         # Only load the necessary columns.
#         data = (
#             row['Outlet Code'],
#             row['Obs Date (yyyy-MM-dd)'],
#             product_name,
#         )
# 
#         dataset.append(data)
# 
#     return dataset

def transform_data(data):
    transformed_data = []
    for row in data:
        # Remove the whitespace from the line.
        row = row.strip()

        # Strip the unnecessary characters added by PostgreSQL.
        row = row[2:-2]

        # Split the row into 3 items.
        row = row.split(',', 2)

        # Remove the list of items from the row.
        items = row.pop()

        # Strip the quotation marks added by PostgreSQL.
        items = items[2:-2]

        # Remove the quotation marks present in the original product names.
        items = items.replace(',', '')

        # Split the items on the custom delimiter
        items = items.split('|')

        # Re-insert the purchased items as a list.
        row.extend(items)

        transformed_data.append(row)

    return transformed_data

def main():
    data = []

    # Open the CSV file with the main dataset and read it into memory as a set
    # of tuples.
    with open(DATA_FILE, 'r') as f:
        print("Loading data from file")
        data = f.readlines()

    print("Transforming data")
    data = transform_data(data)

    # Write the resulting transformed data to a CSV
    print("Writing out transformed data")
    with open(OUT_FILE, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='', quoting=csv.QUOTE_NONE,
                            escapechar='\\')
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    main()

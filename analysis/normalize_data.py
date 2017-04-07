#!/usr/bin/env python3

import csv, re

DATA_FILE='location-kenya.csv'
OUT_FILE='location-kenya_formatted.csv'

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
                            quotechar='', quoting=csv.QUOTE_NONE)
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    main()

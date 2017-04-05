# CSI4142-Project

## Instructions

These instructions assume you are working on Linux.

### Initialize the DB

1. Create the `csi4142` user:

    ```sh
    createuser --interactive
    ```

2. Create the `csi4142` database:

    ```sh
    createdb -U csi4142 csi4142
    ```

3. Initialize the SQL schema:

    ```sh
    psql -U csi4142 -d csi4142 -a -f sql_schema.sql
    ```

### Load the `Date` Values

Loading the dates from the data set into the database:

1. Obtain the [datasets](#datasets)
2. Ensure python is available and installed
3. Setup a virtual environment:

    ```sh
    python3 -m venv venv
    ```

4. Enter the virtual environment:

    ```sh
    source venv/bin/activate
    ```

5. Install the requirements with `pip`:

    ```sh
    pip install -r requirements.txt
    ```

6. Modify the SQL connection parameters as necessary in the `load_date.py`
   script.
7. Run the script:

    ```sh
    ./load_date.py
    ```

### Data Staging via ETL

This uses the ETL script provided to load the remainder of the data into the
database.

1. Perform steps 1-5 from the section above, to setup Python.
2. Modify the SQL connection parameters and other settings as necessary in the
   `etl.py` script.
3. Run the script:

    ```sh
    ./etl.py
    ```

### Analysis with Apriori

This library inclues the [Apriori algorithm implementation][apriori] written by
asaini.

Per the given instructions, we are only interested in analyzing a subset of the
data. As such, the relevant data must first be extracted from PostgreSQL.

**NOTE**: extracted data for `location_key` 167 and all `location_key`s in Kenya
already exist in this repository (see [datasets](#datasets)), so the following
steps are unnecessary unless you are looking to generate custom data.

Extracting data from PostgreSQL for analysis:

1. Modify the following SQL command as necessary, to get the data for either a
   specific location, or for the whole country:

    ```sql
    \copy(
        SELECT (pr.location_key, d.date, array_to_string(array_agg(p.product_name), '|'))
        FROM Product p, ProductPrice pr, Date d, Location l
        WHERE d.date_key = pr.date_key
            AND p.product_key = pr.product_key
            AND pr.location_key = l.location_key
            AND l.country = 'Kenya'
            AND l.location_key = '167'
            GROUP BY (pr.locaton_key, d.date)
    )
    To
    '/tmp/location-167.csv' With CSV;
    ```

2. Extract the data to a temporary file using the above command, modified as
   necessary.
3. Normalize the data with the `analysis/normalize_data.py` script:

    ```sh
    ./normalize_data.py
    ```

4. Analyze the data using the included `analysis/apriori.py` script, setting
   your "support" and "confidence" variables as necessary:

   ```sh
   ./apriori.py -f location-167_formatted.csv -s 0.94 -c 0.68
   ```

**NOTE**: the `apriori.py` script, unlike all the other scripts in this repo,
***REQUIRES*** Python 2 to function.

## Datasets

* [Main][dataset]
* [GNI][gni_dataset]
* [GDP][gdp_dataset]
* [Life expectancy][life_expectancy_dataset]
* Nutrition (included in repo)
* [Population][pop_dataset]

The `location-167_formatted.csv` and `location-kenya_formatted.csv` data sets
are modified representations of the original data set, generated using the
process described in [analysis with Apriori](#analysis-with-apriori). They are
provided to reduce the burden on the user.

### Notes

The GDP, GNI, life expectancy, and population datasets contain a header which
needs to be removed from the CSV files prior to the running the ETL script. Do
not remove the list of column headers from the files.

[apriori]: https://github.com/asaini/Apriori
[gni_dataset]: http://data.worldbank.org/indicator/NY.GNP.PCAP.CD
[dataset]: http://data.worldbank.org/data-catalog/crowd-sourced-price-collection
[gdp_dataset]: http://data.worldbank.org/indicator/NY.GDP.MKTP.CD
[life_expectancy_dataset]: http://data.worldbank.org/indicator/SP.DYN.LE00.IN
[pop_dataset]: http://data.worldbank.org/indicator/SP.POP.TOTL

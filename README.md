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
## Datasets

* [Main][dataset]
* [GDP][gdp_dataset]

### Notes

The GDP dataset contains a header which needs to be removed from the CSV file
prior to the running the ETL script. Do not remove the list of column headers.

[dataset]: http://data.worldbank.org/data-catalog/crowd-sourced-price-collection
[gdp_dataset]: http://data.worldbank.org/indicator/NY.GDP.MKTP.CD

# CSI4142-Project

## Instructions

These instructions assume you are working on Linux.

Loading the dates from the data set into the database:

1. Obtain [the dataset][dataset]
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

[dataset]: http://data.worldbank.org/data-catalog/crowd-sourced-price-collection

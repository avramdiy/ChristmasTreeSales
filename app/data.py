from flask import Flask, jsonify
import pandas as pd
from tableauhyperapi import HyperProcess, Connection, Telemetry, TableName

# Flask app setup
app = Flask(__name__)

# Path to the Hyper file
hyper_file_path = r"C:\Users\Ev\Desktop\Christmas Tree Sales\US Christmas Tree Sales 2010 to 2016.hyper"

def load_hyper_to_dataframe(hyper_file_path):
    """
    Load data from a Hyper file into a Pandas DataFrame.
    """
    try:
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(endpoint=hyper.endpoint, database=hyper_file_path) as connection:
                # Get the first table in the default schema
                tables = connection.catalog.get_table_names(schema="Extract")
                if not tables:
                    raise ValueError("No tables found in the Hyper file.")

                table = tables[0]
                print(f"Loading data from table: {table}")

                # Fetch column names
                table_definition = connection.catalog.get_table_definition(table)
                column_names = [str(col.name) for col in table_definition.columns]  # Ensure column names are strings

                # Fetch rows using a 'with' statement for the Result object
                with connection.execute_query(f"SELECT * FROM {table}") as result:
                    rows = [list(row) for row in result]  # Extract rows into a list
                    dataframe = pd.DataFrame(rows, columns=column_names)

                return dataframe
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Load data into a global variable (or reload it dynamically in routes)
try:
    dataframe = load_hyper_to_dataframe(hyper_file_path)
except Exception as e:
    print(f"Error loading data: {e}")
    dataframe = pd.DataFrame()  # Load an empty DataFrame if the loading fails

@app.route("/data", methods=["GET"])
def get_data():
    """
    Flask route to return the data as JSON.
    """
    if dataframe.empty:
        return jsonify({"error": "No data available"}), 500
    return jsonify(dataframe.to_dict(orient="records"))  # Convert DataFrame to JSON and return it

if __name__ == "__main__":
    app.run(debug=True)

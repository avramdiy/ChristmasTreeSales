from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px

# Flask app setup
app = Flask(__name__, template_folder=r"C:\\Users\\Ev\\Desktop\\Christmas Tree Sales\\templates")

# Path to the CSV file
csv_file_path = r"C:\\Users\\Ev\\Desktop\\Christmas Tree Sales\\US Christmas Tree Sales 2010 to 2016.csv"

def load_csv_to_dataframe(csv_file_path):
    """
    Load data from a CSV file into a Pandas DataFrame and ensure correct types for visualization.
    """
    try:
        # Load CSV into DataFrame
        dataframe = pd.read_csv(csv_file_path)
        
        # Remove the 'index' column if it's included as a feature
        if 'index' in dataframe.columns:
            dataframe.drop(columns=['index'], inplace=True)
        
        # Convert columns to correct types:
        # 'Year' is categorical (can be treated as a string or category)
        dataframe['Year'] = dataframe['Year'].astype(str)
        
        # 'Type of tree' is categorical
        dataframe['Type of tree'] = dataframe['Type of tree'].astype('category')
        
        # Numeric columns: 'Number of trees sold', 'Average Tree Price', 'Sales'
        numeric_columns = ['Number of trees sold', 'Average Tree Price', 'Sales']
        for col in numeric_columns:
            dataframe[col] = pd.to_numeric(dataframe[col], errors='coerce')  # Handle invalid numbers gracefully
        
        # Return cleaned DataFrame
        return dataframe
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

# Load data into global variable (or reload dynamically in routes)
dataframe = load_csv_to_dataframe(csv_file_path)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Flask route to display the chart and handle form submissions.
    """
    columns = dataframe.columns.tolist()  # Get the column names for the dropdown options

    # Pie chart showing proportion of 'Real tree' vs 'Fake tree'
    tree_type_count = dataframe['Type of tree'].value_counts()
    fig = px.pie(names=tree_type_count.index, values=tree_type_count.values, title="Real vs Fake Trees Sold")

    # Convert plot to JSON data for front-end rendering
    pie_chart_data = fig.to_json()

    if request.method == "POST":
        x_feature = request.form.get("x_feature")
        y_feature = request.form.get("y_feature")

        # Generate bar chart based on the selected features
        fig = px.bar(dataframe, x=x_feature, y=y_feature, title=f"{y_feature} vs {x_feature}")
        
        # Convert plot to JSON data for front-end rendering
        chart_data = fig.to_json()

        # Return chart data as a JSON response
        return jsonify(chart_data=chart_data)

    # Render the initial page with available columns, chart, and table data
    return render_template("index.html", columns=columns, chart_data=None, pie_chart_data=pie_chart_data, data=dataframe.to_dict(orient='records'))

@app.route("/data", methods=["GET"])
def get_data():
    """
    Flask route to load the CSV data into a DataFrame and return it as JSON.
    """
    try:
        # Reload the CSV file into the DataFrame
        dataframe = load_csv_to_dataframe(csv_file_path)

        # Convert DataFrame to a dictionary
        data_dict = dataframe.to_dict(orient="records")

        # Return the data as a JSON response
        return jsonify(data_dict)
    except Exception as e:
        return jsonify({"error": f"An error occurred while loading data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px

# Flask app setup with a custom template folder path
app = Flask(__name__, template_folder=r"C:\\Users\\Ev\\Desktop\\Christmas Tree Sales\\templates")

# Path to the CSV file
csv_file_path = r"C:\\Users\\Ev\\Desktop\\Christmas Tree Sales\\US Christmas Tree Sales 2010 to 2016.csv"

def load_csv_to_dataframe(csv_file_path):
    """
    Load data from a CSV file into a Pandas DataFrame.
    """
    try:
        # Load the CSV file into the dataframe, ensuring the first column is not treated as an index
        dataframe = pd.read_csv(csv_file_path, index_col=None)
        
        # Reset the index in case there are any hidden index columns
        dataframe.reset_index(drop=True, inplace=True)
        
        # Convert necessary columns to numeric
        numeric_columns = ['Number of trees sold', 'Average Tree Price', 'Sales']
        dataframe[numeric_columns] = dataframe[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return dataframe
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Load data into a global variable (or reload it dynamically in routes)
dataframe = load_csv_to_dataframe(csv_file_path)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Flask route to display both the pie chart, bar charts, and data.
    """
    # Group the data by Year and Type of tree and sum the 'Number of trees sold'
    grouped_data = dataframe.groupby(['Year', 'Type of tree'])['Number of trees sold'].sum().reset_index()

    # Generate the pie chart for the distribution of real vs fake trees
    pie_data = dataframe['Type of tree'].value_counts().reset_index()
    pie_data.columns = ['Type of tree', 'Count']
    fig_pie = px.pie(pie_data, names='Type of tree', values='Count', title="Real vs Fake Tree Distribution")
    pie_chart_data = fig_pie.to_json()

    # Generate the bar chart for the number of trees sold by year and type
    fig_bar = px.bar(grouped_data, x="Year", y="Number of trees sold", color="Type of tree", 
                     title="Number of Trees Sold by Year and Type", labels={"Number of trees sold": "Number of Trees Sold"})
    bar_chart_data = fig_bar.to_json()

    # Calculate the average tree price per year
    avg_price_by_year = dataframe.groupby('Year')['Average Tree Price'].mean().reset_index()
    
    # Generate the bar chart for average tree price by year
    fig_avg_price = px.bar(avg_price_by_year, x="Year", y="Average Tree Price", 
                           title="Average Tree Price by Year", labels={"Average Tree Price": "Average Price ($)"})
    avg_price_chart_data = fig_avg_price.to_json()

    # Calculate the total sales per year
    sales_by_year = dataframe.groupby('Year')['Sales'].sum().reset_index()

    # Generate the bar chart for total sales by year
    fig_sales = px.bar(sales_by_year, x="Year", y="Sales", 
                       title="Total Sales by Year", labels={"Sales": "Total Sales ($)"})
    sales_chart_data = fig_sales.to_json()

    return render_template("index.html", 
                           pie_chart_data=pie_chart_data, 
                           bar_chart_data=bar_chart_data,
                           avg_price_chart_data=avg_price_chart_data,
                           sales_chart_data=sales_chart_data)

if __name__ == "__main__":
    app.run(debug=True)

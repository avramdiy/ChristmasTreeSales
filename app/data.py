from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# Flask app setup with a custom template folder path
app = Flask(__name__, template_folder=r"C:\\Users\\Ev\Desktop\\Christmas Tree Sales\\templates")

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
        
        # Convert relevant columns to numeric
        dataframe['Year'] = pd.to_numeric(dataframe['Year'], errors='coerce')
        dataframe['Average Tree Price'] = pd.to_numeric(dataframe['Average Tree Price'], errors='coerce')

        return dataframe
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error


def predict_tree_price(dataframe):
    """
    Predict the average tree price for the years 2017-2024 using linear regression.
    """
    # Filter data to use years 2010-2016 for training
    train_data = dataframe[dataframe['Year'] <= 2016]

    # Prepare the data for regression
    X_train = train_data[['Year']]  # Independent variable (Year)
    y_train = train_data['Average Tree Price']  # Dependent variable (Average Tree Price)

    # Initialize the regression model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Predict for the years 2017-2024
    years_to_predict = np.array([[year] for year in range(2017, 2025)])
    predicted_prices = model.predict(years_to_predict)

    # Create a DataFrame with the predictions
    predictions_df = pd.DataFrame({
        'Year': range(2017, 2025),
        'Predicted Average Tree Price': predicted_prices
    })

    return predictions_df


# Load data into a global variable (or reload it dynamically in routes)
dataframe = load_csv_to_dataframe(csv_file_path)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Flask route to display the chart and handle form submissions.
    """
    columns = dataframe.columns.tolist()  # Get the column names for the dropdown options

    # Generate the predicted average tree prices
    predictions_df = predict_tree_price(dataframe)

    # Create a bar chart for the predicted average tree prices
    predicted_fig = px.bar(predictions_df, x='Year', y='Predicted Average Tree Price',
                           title='Predicted Average Tree Price for 2017-2024')

    # Pie chart showing real vs fake trees
    tree_type_counts = dataframe['Type of tree'].value_counts()
    pie_fig = px.pie(names=tree_type_counts.index, values=tree_type_counts.values,
                     title='Tree Type Distribution: Real vs Fake Trees')

    # Bar chart for the number of trees sold
    trees_sold_fig = px.bar(dataframe, x='Year', y='Number of trees sold',
                            title='Number of Trees Sold by Year')

    # Bar chart for the average tree price
    avg_tree_price_fig = px.bar(dataframe, x='Year', y='Average Tree Price',
                                title='Average Tree Price by Year')

    # Bar chart for sales
    sales_fig = px.bar(dataframe, x='Year', y='Sales', title='Sales by Year')

    # Convert the charts to JSON
    pie_chart_data = pie_fig.to_json()
    trees_sold_chart_data = trees_sold_fig.to_json()
    avg_tree_price_chart_data = avg_tree_price_fig.to_json()
    sales_chart_data = sales_fig.to_json()
    predicted_chart_data = predicted_fig.to_json()

    return render_template("index.html",
                           columns=columns,
                           pie_chart_data=pie_chart_data,
                           trees_sold_chart_data=trees_sold_chart_data,
                           avg_tree_price_chart_data=avg_tree_price_chart_data,
                           sales_chart_data=sales_chart_data,
                           predicted_chart_data=predicted_chart_data)


if __name__ == "__main__":
    app.run(debug=True)

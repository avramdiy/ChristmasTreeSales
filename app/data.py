from flask import Flask, render_template, request, jsonify, send_file
from sklearn.linear_model import LinearRegression
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import pandas as pd
import numpy as np
import plotly.express as px

app = Flask(__name__, template_folder=r"C:\\Users\\Ev\\Desktop\\Christmas Tree Sales\\templates")

csv_file_path = r"C:\\Users\\Ev\\Desktop\\Christmas Tree Sales\\US Christmas Tree Sales 2010 to 2016.csv"

# Load and clean the data
def load_csv_to_dataframe(csv_file_path):
    dataframe = pd.read_csv(csv_file_path)
    dataframe.reset_index(drop=True, inplace=True)
    numeric_columns = ['Number of trees sold', 'Average Tree Price', 'Sales']
    dataframe[numeric_columns] = dataframe[numeric_columns].apply(pd.to_numeric, errors='coerce')
    return dataframe

dataframe = load_csv_to_dataframe(csv_file_path)

@app.route("/", methods=["GET"])
def index():
    # Pie chart data
    pie_data = dataframe.groupby('Type of tree')['Number of trees sold'].sum().reset_index()
    pie_chart_data = {
        'values': pie_data['Number of trees sold'].tolist(),
        'labels': pie_data['Type of tree'].tolist(),
        'type': 'pie'
    }

    # Bar chart: Trees sold per year
    bar_chart_trees_sold = {
        'x': dataframe['Year'].tolist(),
        'y': dataframe['Number of trees sold'].tolist(),
        'type': 'bar'
    }

    # Bar chart: Average tree price per year
    bar_chart_avg_price = {
        'x': dataframe['Year'].tolist(),
        'y': dataframe['Average Tree Price'].tolist(),
        'type': 'bar'
    }

    # Bar chart: Sales per year
    bar_chart_sales = {
        'x': dataframe['Year'].tolist(),
        'y': dataframe['Sales'].tolist(),
        'type': 'bar'
    }

    # Predict average tree price for 2017-2024
    years = dataframe['Year'].unique().reshape(-1, 1)
    prices = dataframe.groupby('Year')['Average Tree Price'].mean().values
    model = LinearRegression().fit(years, prices)
    future_years = np.arange(2017, 2025).reshape(-1, 1)
    predicted_prices = model.predict(future_years)

    predicted_bar_chart = {
        'x': future_years.flatten().tolist(),
        'y': predicted_prices.tolist(),
        'type': 'bar'
    }

    return render_template(
        "index.html",
        pie_chart_data=pie_chart_data,
        bar_chart_trees_sold=bar_chart_trees_sold,
        bar_chart_avg_price=bar_chart_avg_price,
        bar_chart_sales=bar_chart_sales,
        predicted_bar_chart=predicted_bar_chart,
        future_years=future_years.flatten().tolist(),
        predicted_prices=predicted_prices.tolist(),
        data=dataframe.to_dict(orient='records')
    )

@app.route("/download_report", methods=["GET"])
def download_report():
    try:
        # Recalculate predictions for 2017-2024
        years = dataframe['Year'].unique().reshape(-1, 1)
        prices = dataframe.groupby('Year')['Average Tree Price'].mean().values
        model = LinearRegression().fit(years, prices)
        future_years = np.arange(2017, 2025).reshape(-1, 1)
        predicted_prices = model.predict(future_years)

        # Create an in-memory buffer
        buffer = BytesIO()

        # Generate the PDF
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 750, "Christmas Tree Sales Summary Report")
        pdf.drawString(100, 730, "This report contains a summary of the dataset and predictions.")

        # Include key statistics
        pdf.drawString(100, 700, f"Total Real Trees Sold: {dataframe[dataframe['Type of tree'] == 'Real tree']['Number of trees sold'].sum()}")
        pdf.drawString(100, 680, f"Total Fake Trees Sold: {dataframe[dataframe['Type of tree'] == 'Fake tree']['Number of trees sold'].sum()}")

        # Include predictions
        pdf.drawString(100, 660, "Predicted Average Tree Prices (2017-2024):")
        y_position = 640
        for year, price in zip(range(2017, 2025), predicted_prices):
            pdf.drawString(120, y_position, f"{year}: ${price:.2f}")
            y_position -= 20

        # Save the PDF
        pdf.save()

        # Move buffer to the beginning
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name="Christmas_Tree_Sales_Report.pdf", mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

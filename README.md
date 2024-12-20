# Project: Christmas Tree Sales Analysis

- This project involves analyzing historical Christmas tree sales data using Tableau and a Flask API. The data is stored in a Tableau Hyper file and is accessed programmatically for analysis and visualization.

## First Commit: Data Loading Functionality

- Setting up the data.py script to connect to the Tableau Hyper API.

- Implementing a function to extract data from the Hyper file located at C:\Users\Ev\Desktop\Christmas Tree Sales\US Christmas Tree Sales 2010 to 2016.hyper.

- Managing resources efficiently with with statements for the HyperProcess and Connection objects.

- Ensuring proper error handling in case the Hyper file is inaccessible or contains no tables.

## Key Features:

- Loads data from the first table in the "Extract" schema of the Hyper file.

- Converts the table data into a Pandas DataFrame for further analysis.

## Second Commit: Exploring the Dataset & Displaying A Visualization

- Swapped hyper file to CSV, found dataset was too small for proper bar chart or scatter plot, initiated index.html and data.py route to show comparison of real or fake trees sold in a pie chart.

## Third Commit: Generating Additional Visualizations

- Generated three additional bar charts. "Number of Trees Sold by Year & Type", "Average Tree Price by Year", "Total Sales by Year"

## Fourth Commit: Linear Regression Model to Predict the Average Tree Price over the Next Decade

- Added a linear regression model to predict average tree prices for the years 2017-2024 based on historical data.

- Integrated the predictions into a new bar chart visualization and updated the Flask data.py to serve the predicted data.

- Modified index.html to display the predicted bar chart alongside the existing charts for a comprehensive view. This enhancement provides insights into future trends in average tree prices.

## Fifth Commit: Providing A Downloadable PDF of All Charts

- Added a /download_report route to generate a downloadable PDF report summarizing the dataset and predicted tree prices for 2017-2024.

- The report includes total real and fake trees sold, along with predictions for average tree prices in a formatted, user-friendly layout.
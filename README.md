# Project: Christmas Tree Sales Analysis

- This project involves analyzing historical Christmas tree sales data using Tableau and a Flask API. The data is stored in a Tableau Hyper file and is accessed programmatically for analysis and visualization.

# First Commit: Data Loading Functionality

- Setting up the data.py script to connect to the Tableau Hyper API.

- Implementing a function to extract data from the Hyper file located at C:\Users\Ev\Desktop\Christmas Tree Sales\US Christmas Tree Sales 2010 to 2016.hyper.

- Managing resources efficiently with with statements for the HyperProcess and Connection objects.

- Ensuring proper error handling in case the Hyper file is inaccessible or contains no tables.

# Key Features:

- Loads data from the first table in the "Extract" schema of the Hyper file.

- Converts the table data into a Pandas DataFrame for further analysis.


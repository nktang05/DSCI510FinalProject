import sqlite3
import pandas as pd
import streamlit as st

# Define the function to feed state data into the database
def feed_state_data(filename, table_name):
    # Establish connection to SQLite database
    conn = sqlite3.connect('tang.db')
    cur = conn.cursor()

    # Read Excel file into a DataFrame
    data = pd.read_excel(filename)
    data.dropna(inplace=True)

    # Write DataFrame to SQLite table
    data.to_sql(table_name, conn, if_exists='replace', index=False)

    # Execute a query to fetch some data from the table (for testing)
    cur.execute(f'SELECT * FROM {table_name} LIMIT 2')
    return_val = cur.fetchall()
    print(return_val)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Define the function to get state data
def get_state_data():
    # Get state data from Excel
    statexlsx = "states.xlsx"
    feed_state_data(statexlsx, "states")

# Call the function to get state data
get_state_data()

conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = conn.cursor()

## Your code here

sql_query9 = "SELECT Name From states Where Region = 'West' "

# Execute the SQL query and load the results into a DataFrame
data9 = pd.read_sql(sql_query9, conn)

st.write(data9)

print(data9)

conn.commit()
conn.close()
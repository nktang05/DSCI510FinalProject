import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine



st.write("hello World")

foodItem = st.text_input("Enter Food Type")
st.write("Your chosen food item", foodItem)

myDict = {1: "one", 2: "two", 3: "three", 4: "four"}

optionsList = list(myDict.values())

option = st.selectbox(
    'What option would you like?',
    optionsList)

selected_key = next(key for key, value in myDict.items() if value == option)

"""
st.write('You selected Series ID:', selected_key)
st.write("You selected Food Item: ", option)

st.image('testing.png', caption="testing stuff")
"""

fig = plt.figure() 
plt.plot([1, 2, 3, 4, 5]) 

st.pyplot(fig)

# Define the function to feed state data into the database
def feed_state_data(filename, table_name):
    # Create SQLAlchemy engine
    engine = create_engine('sqlite:///tang.db', echo=False)

    # Read Excel file into a DataFrame
    data = pd.read_excel(filename)
    data.dropna(inplace=True)

    # Write DataFrame to SQLite table
    data.to_sql(table_name, engine, if_exists='replace', index=False)

    # Execute a query to fetch some data from the table (for testing)
    query_result = engine.execute(f'SELECT * FROM {table_name} LIMIT 2').fetchall()
    print(query_result)

# Define the function to get state data
def get_state_data():
    # Get state data from Excel
    statexlsx = "states.xlsx"
    feed_state_data(statexlsx, "states")

# Call the function to get state data
get_state_data()

# Create SQLAlchemy engine
engine = create_engine('sqlite:///tang.db', echo=False)

## Your code here

sql_query9 = "SELECT Name FROM states WHERE Region = 'West'"

# Execute the SQL query and load the results into a DataFrame
data9 = pd.read_sql(sql_query9, engine)

st.write(data9)

print(data9)
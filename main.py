import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3



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

# method to get state and region data as states
def get_state_data():
    # Get state data from excel
    statexlsx = "states.xlsx"
    df1 = pd.read_excel(statexlsx)
    df1.dropna(inplace=True)

    def feed_state_data(filename, table_name):
        conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()

        # make data fram
        data = pd.read_excel(filename)
        data.dropna(inplace=True)

        # set to sql table
        data.to_sql(table_name, conn, if_exists='replace')
        
        cur.execute(f'SELECT * FROM {table_name} LIMIT 2')
        return_val = cur.fetchall()
        print(return_val)

        conn.commit()
        conn.close()

    feed_state_data(statexlsx, "states")

conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = conn.cursor()

## Your code here

sql_query9 = "SELECT Name From states Where Region = 'West' "

# Execute the SQL query and load the results into a DataFrame
data9 = pd.read_sql(sql_query9, conn)

print(data9)
st.write(data9)

conn.commit()
conn.close()
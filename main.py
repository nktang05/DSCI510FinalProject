

import streamlit as st
import sqlite3
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import requests
from bs4 import BeautifulSoup
import seaborn as sns

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

# method to load in obestiy data as obesity_health
def get_obesity_data():
    # import csv files

    file = "Nutrition__Physical_Activity__and_Obesity_-_Behavioral_Risk_Factor_Surveillance_System_20240412.csv"
    df1 = pd.read_csv(file, header = 0, usecols=[1,3,5,7,10,16])
    df1.dropna(inplace=True)

    def feed_csv_data(filename, table_name):
        conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        df = pd.read_csv(filename)

        # make data fram
        df1 = pd.read_csv(filename, header = 0, usecols=[1,3,5,7,10,16])
        df1.dropna(inplace=True)

        # set to sql table
        df1.to_sql(table_name, conn, if_exists='replace')
        
        cur.execute(f'SELECT * FROM {table_name} LIMIT 2')
        return_val = cur.fetchall()
        print(return_val)

        conn.commit()
        conn.close()

    feed_csv_data(file, "obesity_health")

# method to get population data as population
def get_pop_data():
    # get api data

    key = "d57dfb3474ecd922cc1c04161f67290ae9f3c25d"
    url2019 = f" https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=state:*&key={key}"
    url2018 = f" https://api.census.gov/data/2018/pep/population?get=GEONAME,POP&for=state:*&key={key}"
    url2017 = f" https://api.census.gov/data/2017/pep/population?get=GEONAME,POP&for=state:*&key={key}"
    url2016 = f" https://api.census.gov/data/2016/pep/population?get=GEONAME,POP&for=state:*&key={key}"
    url2015 = f" https://api.census.gov/data/2015/pep/population?get=GEONAME,POP&for=state:*&key={key}"
    url2014 = f" https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&for=state:*&DATE_=6&key={key}"
    url2013 = f" https://api.census.gov/data/2013/pep/natstprc?get=STNAME,POP&for=state:*&DATE_=6&key={key}"
    urlxlsx = "https://www2.census.gov/programs-surveys/popest/tables/2020-2023/state/totals/NST-EST2023-POP.xlsx"

    #2019
    r_data2019 = requests.get(url2019).json()
    df_2019 = pd.DataFrame(r_data2019[1:], columns=r_data2019[0])
    df_2019.drop(['state'], axis=1, inplace=True)
    df_2019['POP'].apply(lambda x: int(x))
    df_2019.rename(columns = {'NAME': 'Region', 'POP':2019}, inplace = True)
    df_2019.set_index('Region')

    #2018
    r_data2018 = requests.get(url2018).json()
    df_2018 = pd.DataFrame(r_data2018[1:], columns=r_data2018[0])
    df_2018.drop(['state'], axis=1, inplace=True)
    df_2018['POP'].apply(lambda x: int(x))
    df_2018.rename(columns = {'GEONAME': 'Region', 'POP':2018}, inplace = True)
    df_2018.set_index('Region')

    #2017
    r_data2017 = requests.get(url2017).json()
    df_2017 = pd.DataFrame(r_data2017[1:], columns=r_data2017[0])
    df_2017.drop(['state'], axis=1, inplace=True)
    df_2017['POP'].apply(lambda x: int(x))
    df_2017.rename(columns = {'GEONAME': 'Region', 'POP':2017}, inplace = True)
    df_2017.set_index('Region')

    #2016
    r_data2016 = requests.get(url2016).json()
    df_2016 = pd.DataFrame(r_data2016[1:], columns=r_data2016[0])
    df_2016.drop(['state'], axis=1, inplace=True)
    df_2016['POP'].apply(lambda x: int(x))
    df_2016.rename(columns = {'GEONAME': 'Region', 'POP':2016}, inplace = True)
    df_2016.set_index('Region')

    #2015
    r_data2015 = requests.get(url2015).json()
    df_2015 = pd.DataFrame(r_data2015[1:], columns=r_data2015[0])
    df_2015.drop(['state'], axis=1, inplace=True)
    df_2015['POP'].apply(lambda x: int(x))
    df_2015['GEONAME'] = df_2015['GEONAME'].apply(lambda x: x.split(',')[0])
    df_2015.rename(columns = {'GEONAME': 'Region', 'POP':2015}, inplace = True)
    df_2015.set_index('Region')

    #2014
    r_data2014 = requests.get(url2014).json()
    df_2014 = pd.DataFrame(r_data2014[1:], columns=r_data2014[0])
    df_2014.drop('DATE_', axis = 1, inplace = True)
    df_2014.drop(['state'], axis=1, inplace=True)
    df_2014['POP'].apply(lambda x: int(x))
    df_2014['STNAME'] = df_2014['STNAME'].apply(lambda x: x.replace('Puerto Rico Commonwealth', 'Puerto Rico'))
    df_2014.rename(columns = {'STNAME': 'Region', 'POP':2014}, inplace = True)
    df_2014.set_index('Region')

    #2013
    r_data2013 = requests.get(url2013).json()
    df_2013 = pd.DataFrame(r_data2013[1:], columns=r_data2013[0])
    df_2013.drop(['state'], axis=1, inplace=True)
    df_2013.drop('DATE_', axis = 1, inplace = True)
    df_2013['POP'].apply(lambda x: int(x))
    df_2013['STNAME'] = df_2013['STNAME'].apply(lambda x: x.replace('Puerto Rico Commonwealth', 'Puerto Rico'))
    df_2013.rename(columns = {'STNAME': 'Region', 'POP':2013}, inplace = True)
    df_2013.set_index('Region')

    df1 = pd.read_excel(urlxlsx, header = 3, nrows = 58)

    df1.rename(columns = {df1.columns[0]:'Region', df1.columns[1]:'Base'}, inplace = True)
    df1.dropna(inplace=True)
    df1.drop('Base', axis=1, inplace=True)
    df1['Region'] = df1['Region'].apply(lambda x: x.replace('.', ''))
    df1.set_index('Region')

    df1[2020] = df1[2020].apply(lambda x: int(x))
    df1[2021] = df1[2021].apply(lambda x: int(x))
    df1[2022] = df1[2022].apply(lambda x: int(x))
    df1[2023] = df1[2023].apply(lambda x: int(x))

    data = pd.merge(df_2013, df_2014)
    data = pd.merge(data, df_2015)
    data = pd.merge(data, df_2016)
    data = pd.merge(data, df_2017)
    data = pd.merge(data, df_2018)
    data = pd.merge(data, df_2019)
    data = pd.merge(data, df1)

    def feed_api_data(data, table_name):
        conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()

        
        # set to sql table
        data.to_sql(table_name, conn, if_exists='replace')

        ### Your code ends here ###
        
        cur.execute(f'SELECT * FROM {table_name} LIMIT 2')
        return_val = cur.fetchall()
        print(return_val)

        conn.commit()
        conn.close()

    feed_api_data(data, "population")

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

# method for series data as table seriesId
def get_series_data():
    # webscraping data
    url = "https://beta.bls.gov/dataQuery/find?fq=survey:[ap]"
    r = requests.get(url)
    r.content
    soup = BeautifulSoup(r.content, 'lxml')
    itemsx = soup.find('body').find_all('div', {'class': 'dq-result-item'})
    itemlist = ['Series Title', 'Series ID', 'Survey Name', 'Measure Data Type', 'Area', 'Item']
    data = []
    for item in itemsx:
        dat = {}
        rows = item.find('table').find('tbody').find_all('tr')
        for row in rows:
            dat[row.find('th').contents[0]] = row.find('td').contents[0]
        data.append(dat)

    maxpage = 100
    page = 1
    data = []
    stop = False
    url = 'https://beta.bls.gov/dataQuery/find?fq=survey:[ap]'

    while (page < maxpage) and (stop is False):
        
        r = requests.get(url)
        r.content
        soup = BeautifulSoup(r.content, 'lxml')
        
        itemsx = soup.find('body').find_all('div', {'class': 'dq-result-item'})
        
        for item in itemsx:
            dat = {}
            rows = item.find('table').find('tbody').find_all('tr')
            for row in rows:
                dat[row.find('th').contents[0]] = row.find('td').contents[0]
            data.append(dat)

        nextx = soup.find('body').find('div', {'class':'dq-next-page'}).find('a', {'id':'nextlink'})
        if nextx is None:
            stop = True
        else:
            url = 'https://beta.bls.gov/dataQuery/' + nextx['href']
        page += 1

    def feed_web_data(table_name):
        conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()

        maxpage = 100
        page = 1
        data = []
        stop = False
        url = 'https://beta.bls.gov/dataQuery/find?fq=survey:[ap]'

        while (page < maxpage) and (stop is False):
            
            r = requests.get(url)
            r.content
            soup = BeautifulSoup(r.content, 'lxml')
            
            itemsx = soup.find('body').find_all('div', {'class': 'dq-result-item'})
            
            for item in itemsx:
                dat = {}
                rows = item.find('table').find('tbody').find_all('tr')
                for row in rows:
                    dat[row.find('th').contents[0]] = row.find('td').contents[0]
                data.append(dat)

            nextx = soup.find('body').find('div', {'class':'dq-next-page'}).find('a', {'id':'nextlink'})
            if nextx is None:
                stop = True
            else:
                url = 'https://beta.bls.gov/dataQuery/' + nextx['href']
            page += 1


        df = pd.DataFrame(data)

        # set to sql table
        df.to_sql(table_name, conn, if_exists='replace')

        cur.execute(f'SELECT * FROM {table_name} LIMIT 2')
        return_val = cur.fetchall()
        print(return_val)

        conn.commit()
        conn.close()

    feed_web_data("seriesID")

def locationString(location):
    conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    
    if (location == "West" or location == "South" or location == "Northeast" or location == "Midwest"):
        # Query to retrieve the states in the West region
        sql_query9 = """
            SELECT Name
            FROM states
            WHERE Region = ?
        """
    
        # Execute the SQL query to retrieve the states in the West region
        region = pd.read_sql(sql_query9, conn, params=(location,))
        
        # List of state names in the West region
        states = region['Name'].tolist()
        
        # Convert the list of state names to a comma-separated string for the IN clause
        state_names_str = ', '.join([f"'{state}'" for state in states])

    else:
        state_names_str = f"'{location}'"

    # Close the connection
    conn.close()

    return state_names_str

def regionString(location):
    conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    
    if (location != "West" and location != "South" and location != "Northeast" and location != "Midwest"):
        # Query to retrieve the states in the West region
        sql_query9 = """
            SELECT Region
            FROM states
            WHERE Name = ?
        """

        # Execute the SQL query with the state name as a parameter
        cur.execute(sql_query9, (location,))

        # Fetch the result
        region = cur.fetchone()[0]

    else:
        region = location

    # Close the connection
    conn.close()

    return region

# get dict of series id data
def getSeriesIdDict(userItem, location):
    conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    
    state_names_str = regionString(location)
    
    # Use proper string formatting for the user input and location
    sql_query10 = f"""
         SELECT `Series ID`, `Series Title`
        FROM seriesID
        WHERE item LIKE ? AND Area = ?
    """
    
    # Execute the SQL query with the user input as a parameter
    cur.execute(sql_query10, ('%' + userItem + '%', state_names_str))
    
    # Fetch the results
    results = cur.fetchall()
    
    # Execute the SQL query and load the results into a DataFrame
    data10 = pd.DataFrame(results, columns=['Series ID', 'Series Title'])
    
    result_dict = {row[0]: row[1] for row in results}
    
    print(data10)
    
    print(result_dict)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return result_dict

# method for prices of food as 
def grocery(userSeriesId, result_dict):
    url = f"https://data.bls.gov/timeseries/{userSeriesId}?amp%253bdata_tool=XGtable&output_view=data&include_graphs=true"
    food = result_dict[userSeriesId]

    r = requests.get(url)
     #r.content
    soup = BeautifulSoup(r.content, 'lxml')
    t1 = soup.find('table', {"id":"table0"})
    headerx = t1.find('thead').find('tr').find_all('th')
    header = [x.contents[0] for x in headerx]

    table = []
    index = []
    rows = t1.find('tbody').find_all('tr')
    for row in rows:
        datax = row.find_all('td')
        indexx = row.find('th')
        data = [x.contents[0] for x in datax]
        index.append(int(indexx.contents[0]))
        table.append(data)

    df = pd.DataFrame(data = table, index = index, columns = header[1:])

    df_table = pd.DataFrame(columns = ["Year", "Month", "Price"])

    for index, row in df.iterrows():
        for col in df.columns:
            if row[col] is not None:
                df_table.loc[len(df_table)] = [index, col, row[col]]

    def feed_data(df, table_name):
        conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur = conn.cursor()
        
        
        ### Write Your code here ###
        
        # set to sql table
        df.to_sql(table_name, conn, if_exists='replace')

        ### Your code ends here ###
        
        cur.execute(f'SELECT * FROM {table_name} LIMIT 2')
        return_val = cur.fetchall()
        print(return_val)

        conn.commit()
        conn.close()

    feed_data(df_table, userSeriesId)

def groceryTable(table):
    # Connect to the database
    conn = sqlite3.connect('tang.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    
    # Execute the SQL query and load the results into a DataFrame
    sql_query2 = "SELECT * FROM {}".format(table)
    data2 = pd.read_sql(sql_query2, conn)
    
    # Close the connection
    conn.close()
    
    
    
    # Replace empty strings with NaN
    data2['Price'].replace('', pd.NA, inplace=True)
    
    # Convert 'Price' column from string to numeric
    data2['Price'] = pd.to_numeric(data2['Price'], errors='coerce')
    
    # Sort the data frame by 'Year'
    data2_sorted = data2.sort_values(by='Year')
    
    
    # Plot box-and-whisker for max and min prices
    fig = plt.figure(figsize=(10, 6))
    
    # Box-and-whisker plot
    sns.boxplot(x='Year', y='Price', data=data2_sorted, whis=[0, 100])
    plt.title('Box-and-Whisker Plot for Prices of ' + result_dict[table])
    plt.xlabel('Year')
    plt.ylabel('Price')
    
    plt.tight_layout()
    plt.show()

    st.pyplot(fig)


# LOAD ALL DATA
get_obesity_data()
get_pop_data()
get_state_data()
get_series_data()

#OTHER TESTING
region = regionString("West")
result_dict = getSeriesIdDict("beef", region)
grocery("APU0400703112", result_dict)
groceryTable('APU0400703112')

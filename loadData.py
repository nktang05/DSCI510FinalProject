import os
import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd

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


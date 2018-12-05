import pandas as pd
import numpy as np

from selenium.webdriver import (Chrome, Firefox)
import time
import requests
from bs4 import BeautifulSoup
import random


def scrape_huskies(start_year, end_year):

    df = pd.DataFrame()
    for year in range(start_year, end_year+1):
   
        url = f"https://www.sports-reference.com/cfb/schools/washington/{year}-schedule.html"
        sel = "table#schedule"

        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(random.random()*10 + 5)
        table = soup.select_one(sel)
        table_rows = table.select('tr')
        data_rows = []
        for table_row in table_rows:
            th_elements = table_row.select('th')
            th_data = [th.text for th in th_elements]
            td_elements = table_row.select('td')
            td_data = [td.text for td in td_elements]
            data_rows.append(th_data + td_data)        
        new_df = pd.DataFrame(data_rows[1:], columns=data_rows[0])
        df = df.append(new_df)
    
    return df


def scrape_seahawks(start_year, end_year):

    df = pd.DataFrame()
    for year in range(start_year, end_year+1):
   
        url = f"https://www.pro-football-reference.com/teams/sea/{year}.htm"
        sel = "table#games"

        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(random.random()*10 + 5)
        table = soup.select_one(sel)
        table_rows = table.select('tr')
        data_rows = []
        for table_row in table_rows:
            th_elements = table_row.select('th')
            th_data = [th.text for th in th_elements]
            td_elements = table_row.select('td')
            td_data = [td.text for td in td_elements]
            data_rows.append(th_data + td_data)        
        new_df = pd.DataFrame(data_rows[2:], columns=data_rows[1])
        new_df['year'] = year
        df = df.append(new_df)
    
    return df
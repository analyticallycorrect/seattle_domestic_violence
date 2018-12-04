import pandas as pd
import numpy as np
import datetime as dt


class DataRetrieval():
    
    #def __init__(self):

    
    def get_calls_data(self, filepath='../data/Calls_Table_data.csv', delimiter='\t'):
        """Retrieves call data from filepath"""
        df = pd.read_csv(filepath, delimiter='\t', encoding='utf-16')
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)        
        return df
    
    def get_weather_data(self, filepath='../data/historical_weather.csv'):
        """Retrieves weather data from filepath"""
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['DATE']).dt.date
        weather_hist = (df[['date', 'TMAX', 'PRCP', 'SNOW']]
                        .rename(columns={'PRCP':'precip', 'TMAX':'temp_max',
                                         'PRCP':'precip', 'SNOW':'snow'}))
        weather_hist['precip^2'] = weather_hist['precip']**2
        weather_hist['snow^2'] = weather_hist['snow']**2      
        return weather_hist
    
    def get_seahawks_schedule(self, filepath='../data/seahawks_schedule.csv'):
        """
        Retrieves Seahawks game schedule from filepath
        
        Will need to rewrite scraper used to retrieve this data
        """
        df_in = pd.read_csv(filepath)
        df_dropna = df_in.copy()[df_in['Opp'].notna()].reset_index(drop=True)
        df = df_dropna.copy()[df_dropna['Opp'] != 'Bye Week'].reset_index(drop=True)
        
        
        df['date'] = ''
        for i in range(len(df)):
            df['date'][i] = (f"{df.iloc[i]['Date']}, {df.iloc[i]['year']}")
            
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        df['seahawks_game'] = ''
        for i in range(len(df)):
            if type(df.iloc[i]['Unnamed: 10']) == str:
                if df.iloc[i]['Week'] == 'SuperBowl':
                    df['seahawks_game'][i] = 'SuperBowl'
                elif df.iloc[i]['Week'] in ['Wild Card', 'Division','Conf. Champ.']:
                    df['seahawks_game'][i] = 'away_Playoffs'
                else:
                    df['seahawks_game'][i] = 'away_Regular'
            else:     
                if df.iloc[i]['Week'] == 'SuperBowl':
                    df['seahawks_game'][i] = 'SuperBowl'
                elif df.iloc[i]['Week'] in ['Wild Card', 'Division','Conf. Champ.']:
                    df['seahawks_game'][i] = 'home_Playoffs'
                else:
                    df['seahawks_game'][i] = 'home_Regular'
        return df[['date', 'seahawks_game']].copy()
    
    def get_huskies_schedule(self, filepath='../data/huskies_schedule.csv'):
        """
        Retrieves Huskies game schedule from filepath

        Will need to rewrite scraper used to retrieve this data
        """
        df_in = pd.read_csv(filepath)
        df = df_in.copy()
        df['date'] = pd.to_datetime(df['Date']).dt.date

        df['huskies_game'] = ''
        for i in range(len(df)):
            if type(df.iloc[i]['Unnamed: 6']) == str:
                df['huskies_game'][i] = 'away'
            else:
                df['huskies_game'][i] = 'home'
        return df[['date','huskies_game']].copy()

    def get_sounders_schedule(self, filepath='../data/sounders_schedule.csv'):
        """
        Retrieves Sounders FC game schedule from filepath

        Will write instructions for getting game data
        """
        df_in = pd.read_csv(filepath)
        df = df_in.copy()
        df['date'] = pd.to_datetime(df_in['date_dd_mm_yy']).dt.date
        
        df['sounders_game'] = ''
        for i in range(len(df)):
            if df['home_team'][i].split()[0] == 'Seattle':
                df['sounders_game'][i] = 'home'
            else:
                df['sounders_game'][i] = 'away'
        return df[['date','sounders_game']].drop_duplicates()


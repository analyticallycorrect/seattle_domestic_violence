import pandas as pd
import numpy as np
import datetime as dt


class CountCalls():
    """Counts calls by date either by city or neighborhood"""
    
    def __init__(self, how='city'):
        self.how = how
        self.X = None
        self.y = None
        
    def fit(self, X, y=None):
        self.X = X
        self.y = y
        self.how = self.how
        return self
    
    def transform(self, y=None):
        
        if self.how == 'city':
            df = self.X[['ORIG_TIME_QUEUED', 'EVENT']].copy()
            df['date'] = pd.to_datetime(df['ORIG_TIME_QUEUED']).dt.date
            df.drop('ORIG_TIME_QUEUED', axis=1, inplace=True)
            return df.groupby('date').count().rename(columns={'EVENT':'num_calls'}).reset_index()
        
        else:
            df = self.X[['NEIGHBORHOOD', 'ORIG_TIME_QUEUED', 'EVENT']].copy()
            df['date'] = pd.to_datetime(df['ORIG_TIME_QUEUED']).dt.date
            df.drop('ORIG_TIME_QUEUED', axis=1, inplace=True)
            counts = df.groupby(['NEIGHBORHOOD', 'date']).count().rename(columns=
                                                                         {'NEIGHBORHOOD':'neighborhood',
                                                                          'EVENT':'num_calls'}).reset_index()
            
            neighborhoods = list(counts['NEIGHBORHOOD'].unique())
            num_days = int(np.timedelta64((max(counts['date']) - min(counts['date'])), 'D')/np.timedelta64(1,'D'))+1
            start = pd.to_datetime(min(counts['date']))
            neighboor_arr = np.array([(neighborhoods*num_days)])
            neighboor_arr = neighboor_arr.flatten()
            dates = [(start + np.timedelta64(i,'D')) for i in range(num_days)]*len(neighborhoods)
            
            df2 = pd.DataFrame({"dt_time": dates})
            df2['date'] = df2["dt_time"].dt.date
            df2['neighborhood'] = neighboor_arr
            df3 = pd.merge(df2, counts, how='outer', left_on=['date','neighborhood'],
                           right_on=['date','NEIGHBORHOOD']).fillna(0)
            return df3[['date', 'neighborhood', 'num_calls']]
        
        

class FeaturizeCalls():
    """Clean incoming df to fit into model"""
    
    def __init__(self):
        self.X = None
        self.y = None
    
    def fit(self, X, y=None):
        self.X = X
        self.y = y
        return self

    
    def transform(self, y=None):
        """tranform and clean incoming training or test"""
    
        df = self.X.copy()
        num_days = int(np.timedelta64((max(df['date']) - min(df['date'])), 'D')/np.timedelta64(1,'D'))+1
        start = pd.to_datetime(min(df['date']))
        dates = [(start + np.timedelta64(i,'D')) for i in range(num_days)]

        seq = pd.DataFrame({'dt_time': dates, 'day_seq':np.arange(num_days)})
        seq['date'] = seq['dt_time'].dt.date

        df1 = df.join(seq.set_index('date'), on='date')

        df1['year'] = df1['dt_time'].dt.year
        df1['month'] = df1['dt_time'].dt.month
        df1['day'] = df1['dt_time'].dt.day
        df1['day_of_week'] = df1['dt_time'].dt.weekday
        df1['month_day'] = df1['dt_time'].dt.strftime('%m/%d')
        df1['month_weekday'] = df1['dt_time'].dt.strftime('%b_%a')
        df1['month'] = df1['dt_time'].dt.strftime('%m/%d')     
        return df1


class DateDummies():

    def __init__(self):
        self.X = None
        self.y = None
    
    def fit(self, X, y=None):
        # X is the featurized calls dataframe
        self.X = X 
        self.y = y
        return self

    def transform(self, y=None):
        day_features= ['01/06','01/14','02/02','02/07','03/01','03/10','03/20','03/26','04/01','04/08',
                       '04/17','04/18','05/06','05/09','05/10','05/21','05/31','06/04','06/05','06/13',
                       '06/28','06/30','07/09','07/16','07/20','07/23','07/29','08/01','08/20','08/24',
                       '08/28','09/08','09/11','09/14','09/30','10/02','10/17','10/26','11/01','11/15',
                       '11/16','11/23','11/27','12/04','12/12','12/19','12/21','12/23','12/29']
        spec_days = pd.DataFrame({'month_day':day_features, 'spec_day':day_features})
        df =self.X.join(spec_days.set_index('month_day'), on='month_day')

        date_dummies =  pd.get_dummies(df[['date', 'day', 'month_weekday', 'spec_day']].set_index('date'),
                                       columns=['day', 'month_weekday', 'spec_day']).reset_index().drop_duplicates()
        return df.join(date_dummies.set_index('date'), on='date').fillna(0)   
    

class HolidayDummies():
    
    def __init__(self):
        self.X = None
        self.y = None
    
    def fit(self, X, y=None):
        # X is a dictionary of Holidays
        self.X = X 
        self.y = y
        return self

    def transform(self, y=None):
        _holidays = []
        for date in sorted(self.X.keys()):
            _holidays.append([date, self.X[date]])
        _holidays = pd.DataFrame(_holidays, columns=['date', 'holiday'])
        return pd.get_dummies(_holidays.set_index('date')).reset_index()
    
    
class EventDummies():
    
    def __init__(self, event_dict=None):
        self.X = None
        self.y = None
        self.event_dict = event_dict

        defualt_events = ({'Pride Parade' : ['6/30/2019', '6/24/2018', '6/25/2017', '6/26/2016', '6/28/2015',
                                          '6/29/2014', '6/30/2013', '6/24/2012', '6/26/2011', '6/27/2010'],
                            'Seafair' : ['8/2/2019', '8/3/2019', '8/4/2019', '8/3/2018', '8/4/2018', '8/5/2018',
                                         '8/4/2017', '8/5/2017', '8/6/2017', '8/5/2016', '8/6/2016', '8/7/2016',
                                         '7/31/2015', '8/1/2015', '8/2/2015', '8/1/2014', '8/2/2014', '8/3/2014',
                                         '8/2/2013', '8/3/2013', '8/4/2013', '8/3/2012', '8/4/2012', '8/5/2012',
                                         '8/5/2011', '8/6/2011', '8/7/2011', '8/6/2010', '8/7/2010', '8/8/2010' ],
                            'Soltice Parade': ['6/30/2019', '6/16/2018', '6/17/2017', '6/18/2016', '6/20/2015',
                                               '6/21/2014', '6/22/2013', '6/16/2012', '6/18/2011', '6/19/2010'],
                            'Womens March' : ['1/19/2019', '1/20/2018', '1/21/2017'],})
        
        if self.event_dict == None:
            self.event_dict = defualt_events
        
    
    def fit(self, X=None, y=None):
        self.X = X 
        self.y = y
        return self
    
    def transform(self, y=None):
        _events = []
        for event in self.event_dict.keys():
            for day in self.event_dict[event]:
                _events.append([dt.datetime.strptime(day, '%m/%d/%Y'), event])
                
        _events = pd.DataFrame(_events, columns=['date','local_event'])
        _events['date'] = _events['date'].dt.date
        return pd.get_dummies(_events.set_index('date')).reset_index()
    
    
class MakeDummies():
    
    def __init__(self):
        self.X = None
        self.y = None
    
    def fit(self, X, y=None):
        # X is a dataframe of sporting events
        self.X = X 
        self.y = y
        return self

    def transform(self, y=None):
        return pd.get_dummies(self.X.set_index('date')).reset_index()    
        

class JoinDataFrames():
    
    def __init__(self, weather, us_holidays, islamic_holidays, 
                 jewish_holidays, events, seahawks, huskies, sounders):
        self.weather = weather
        self.us_holidays = us_holidays
        self.islamic_holidays = islamic_holidays
        self.jewish_holidays = jewish_holidays
        self.events = events
        self.seahawks = seahawks
        self.huskies = huskies
        self.sounders = sounders
        self.X = None
        self.y = None

    def fit(self, X, y=None):
        self.X = X
        self.y = y
        return self
    
    def transform(self):
        df1 = self.join_dfs(self.X, self.weather)
        df2 = self.join_dfs(df1, self.us_holidays)
        df3 = self.join_dfs(df2, self.islamic_holidays)
        df4 = self.join_dfs(df3, self.jewish_holidays)
        df5 = self.join_dfs(df4, self.events)
        df6 = self.join_dfs(df5, self.seahawks)
        df7 = self.join_dfs(df6, self.huskies)
        df8 = self.join_dfs(df7, self.sounders)
        return df8.fillna(0)
            
    def join_dfs(self, df1, df2):
        return df1.join(df2.set_index('date'), on='date')


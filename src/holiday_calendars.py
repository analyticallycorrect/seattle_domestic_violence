import pandas as pd
import numpy as np
import datetime as dt

import holidays
from calendra.asia import Qatar
from calendra.asia import HongKong

class SeattleHolidays:
    
    
    class CustomHolidays(holidays.US):
        def _populate(self, year=2019, start_year=2009, end_year=2030):
            # Populate the holiday list with the default US holidays
            holidays.US._populate(self, year)
            # Example: Add Ninja Turtle Day
            #self[dt.date(year, 7, 13)] = "Ninja Turtle Day"
            for year in range(start_year, end_year):
                # Add Valentine's day
                self[dt.date(year, 2, 14)] = "Valentines Day"
                # Add St Patricks Day
                self[dt.date(year, 3, 17)] = "St Patricks Day"
                # Add Easter
                self[holidays.easter(year=year)] = "Easter"
                # Add Good Friday
                self[holidays.easter(year=year)  -  dt.timedelta(days=2)] = "Good Friday"
                # Add May Da
                self[dt.date(year, 5, 1)] = "May Day"
                # Add Cinco De Mayo
                self[dt.date(year, 5, 5)] = "Cinco De Mayo"
                # Add Halloween
                self[dt.date(year, 10, 31)] = "Halloween"
                # Add Día de Muertos
                self[dt.date(year, 11, 2)] = "Halloween"
                # Add Christmas Eve
                self[dt.date(year, 12, 24)] = "Christmas Eve"
                # Add New Years Eve
                self[dt.date(year, 12, 31)] = "New Years Eve"
                # Add Chinese New Year
                chinese = HongKong()
                for date, label in chinese.get_chinese_new_year(year):
                    self[date] = label


    class IslamicHolidays(holidays.HolidayBase):
        def _populate(self, year=2019, start_year=2009, end_year=2030):
            qatar_holidays = Qatar()
            # Populate the holiday list with blank base holidays
            holidays.HolidayBase._populate(self, year)
            for year in range(start_year, end_year):
                days = qatar_holidays.get_calendar_holidays(year)
                # Add Ramadan
                for i in range(1, len(days)):
                    if qatar_holidays.get_calendar_holidays(year)[i][1] == 'Start of ramadan':
                        for day in range(30):
                            self[qatar_holidays.get_calendar_holidays(year)[i][0] 
                                 + dt.timedelta(days=day-1)] = "Ramadan"
                    else:
                        self[qatar_holidays.get_calendar_holidays(2018)[1][0] 
                             - dt.timedelta(days=2)] = qatar_holidays.get_calendar_holidays(year)[i][1]


    class JewishHolidays(holidays.HolidayBase):
        def retrieve_data(self, filepath):
            df = pd.read_csv(filepath)
            return df

        def get_holidays(self, paths_list):
            df = self.retrieve_data(paths_list[0])
            for filepath in paths_list[1 : ]:
                cal = self.retrieve_data(filepath)
                df = pd.concat([df, cal])
            return df

        def _populate(self, year=2019, paths_list=['../data/hebcal_2010_usa.csv',
                                                   '../data/hebcal_2015_usa.csv', 
                                                   '../data/hebcal_2020_usa.csv',
                                                   '../data/hebcal_2025_usa.csv'],
                      start_year=2009, end_year=2030):
            hebcal = self.get_holidays(paths_list)
            hebcal.reset_index(drop=True, inplace=True)
            hebcal['date'] = pd.to_datetime(hebcal["Start Date"]).dt.date
            # Populate the holiday list with blank base holidays
            holidays.HolidayBase._populate(self, year)
            for year in range(start_year, end_year):
                for i in range(len(hebcal)):
                    self[hebcal['date'][i]] = hebcal['Subject'][i]


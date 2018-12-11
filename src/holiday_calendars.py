import pandas as pd
import numpy as np
import datetime as dt

import holidays
from calendra.asia import Qatar
from calendra.asia import HongKong


class SeattleHolidays:
    """Classes to create holiday calendars

    Attributes
    -----------
    None
    """
    class CustomHolidays(holidays.US):
        """Creates calendar dictionary of US Christian and Secular holidays

        Attributes
        -----------
        None
        """
        def _populate(self, year=2019, start_year=2009, end_year=2030):
            """Creates calendar dictionary of US Christian and Secular holidays

            Parameters
            -----------
            year: Integer of the current year
            start_year: Integer of the first year used in model
            end_year: Integer of the last year that will be forecasted

            Returns
            --------
            Dictionary
            """
            # Populate the holiday list with the default US holidays
            holidays.US._populate(self, year)
            # Example: Add Ninja Turtle Day
            # self[dt.date(year, 7, 13)] = "Ninja Turtle Day"
            for year in range(start_year, end_year):
                # Add Valentine's day
                self[dt.date(year, 2, 14)] = "Valentines Day"
                # Add St Patricks Day
                self[dt.date(year, 3, 17)] = "St Patricks Day"
                # Add Easter
                self[holidays.easter(year=year)] = "Easter"
                # Add Good Friday
                self[holidays.easter(year=year) - dt.timedelta(days=2)] = "Good Friday"
                # Add May Day
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
        """Creates calendar dictionary of Islamic holidays

        Attributes
        -----------
        None
        """
        def _populate(self, year=2019, start_year=2009, end_year=2030):
            """Creates calendar dictionary of Islamic holidays

            Parameters
            -----------
            year: Integer of the current year
            start_year: Integer of the first year used in model
            end_year: Integer of the last year that will be forecasted

            Returns
            --------
            Dictionary
            """
            qatar_holidays = Qatar()
            # Populate the holiday list with blank base holidays
            holidays.HolidayBase._populate(self, year)
            for year in range(start_year, end_year):
                days = qatar_holidays.get_calendar_holidays(year)
                # Add Ramadan
                for i in range(1, len(days)):
                    if (
                        qatar_holidays.get_calendar_holidays(year)[i][1]
                        == "Start of ramadan"
                    ):
                        for day in range(30):
                            self[
                                qatar_holidays.get_calendar_holidays(year)[i][0]
                                + dt.timedelta(days=day - 1)
                            ] = "Ramadan"
                    else:
                        self[
                            qatar_holidays.get_calendar_holidays(2018)[1][0]
                            - dt.timedelta(days=2)
                        ] = qatar_holidays.get_calendar_holidays(year)[i][1]

    class JewishHolidays(holidays.HolidayBase):
        """Creates calendar dictionary of Jewish holidays

        Attributes
        -----------
        None
        """
        def retrieve_data(self, filepath):
            """Retrieves .csv file containing Jewish holiday data

            Parameters
            -----------
            filepath: file paths for file with calendar data

            Returns
            --------
            Dataframe
            """
            df = pd.read_csv(filepath)
            return df

        def get_holidays(self, paths_list):
            """Creates dataframe of Jewish holiday data

            Parameters
            -----------
            paths_list: file paths for files with calendar data

            Returns
            --------
            Dataframe
            """
            df = self.retrieve_data(paths_list[0])
            for filepath in paths_list[1:]:
                cal = self.retrieve_data(filepath)
                df = pd.concat([df, cal])
            return df

        def _populate(
            self,
            year=2019,
            paths_list=[
                "../data/hebcal_2010_usa.csv",
                "../data/hebcal_2015_usa.csv",
                "../data/hebcal_2020_usa.csv",
                "../data/hebcal_2025_usa.csv",
            ],
            start_year=2009,
            end_year=2030,
        ):
            """Creates calendar dictionary of Jewish holidays

            Parameters
            -----------
            year: Integer of the current year
            paths_list: file paths for files with calendar data
            start_year: Integer of the first year used in model
            end_year: Integer of the last year that will be forecasted

            Returns
            --------
            Dictionary
            """
            hebcal = self.get_holidays(paths_list)
            hebcal.reset_index(drop=True, inplace=True)
            hebcal["date"] = pd.to_datetime(hebcal["Start Date"]).dt.date
            # Populate the holiday list with blank base holidays
            holidays.HolidayBase._populate(self, year)
            for year in range(start_year, end_year):
                for i in range(len(hebcal)):
                    self[hebcal["date"][i]] = hebcal["Subject"][i]

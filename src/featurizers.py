import pandas as pd
import numpy as np
import datetime as dt

from src.holiday_calendars import SeattleHolidays
from src.data_retrievers import DataRetrieval
from src.weather_scraper import seattle_weather_fcst


class CountCalls:
    """Counts calls by date either by city or neighborhood

    Attributes
    -----------
    how: grouping level to count calls by. Either city or neighborhood
    """

    def __init__(self, how="city"):
        """The constructor for CounterCalls class.

        Parameters
        -----------
        how: grouping level to count calls by. Either city or neighborhood
        """

        self.how = how
        self.X = None
        self.y = None

    def fit(self, X, y=None):
        """Fit the calls for service dataframe to be transformed into a dataframe of call counter per day.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        self.X = X
        self.y = y
        self.how = self.how
        return self

    def transform(self, y=None):
        """Transforms the calls for service dataframe into a dataframe of call counter per day.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """

        if self.how == "city":
            df = self.X[["ORIG_TIME_QUEUED", "EVENT"]].copy()
            df["date"] = pd.to_datetime(df["ORIG_TIME_QUEUED"]).dt.date
            df.drop("ORIG_TIME_QUEUED", axis=1, inplace=True)
            return (
                df.groupby("date")
                .count()
                .rename(columns={"EVENT": "num_calls"})
                .reset_index()
            )

        else:
            df = self.X[["NEIGHBORHOOD", "ORIG_TIME_QUEUED", "EVENT"]].copy()
            df["date"] = pd.to_datetime(df["ORIG_TIME_QUEUED"]).dt.date
            df.drop("ORIG_TIME_QUEUED", axis=1, inplace=True)
            counts = (
                df.groupby(["NEIGHBORHOOD", "date"])
                .count()
                .rename(columns={"NEIGHBORHOOD": "neighborhood", "EVENT": "num_calls"})
                .reset_index()
            )

            neighborhoods = list(counts["NEIGHBORHOOD"].unique())
            num_days = (
                int(
                    np.timedelta64((max(counts["date"]) - min(counts["date"])), "D")
                    / np.timedelta64(1, "D")
                )
                + 1
            )
            start = pd.to_datetime(min(counts["date"]))
            neighboor_arr = np.array([(neighborhoods * num_days)])
            neighboor_arr = neighboor_arr.flatten()
            dates = [(start + np.timedelta64(i, "D")) for i in range(num_days)] * len(
                neighborhoods
            )

            df2 = pd.DataFrame({"dt_time": dates})
            df2["date"] = df2["dt_time"].dt.date
            df2["neighborhood"] = neighboor_arr
            df3 = pd.merge(
                df2,
                counts,
                how="outer",
                left_on=["date", "neighborhood"],
                right_on=["date", "NEIGHBORHOOD"],
            ).fillna(0)
            return df3[["date", "neighborhood", "num_calls"]]


class FeaturizeCalls:
    """Adds features to dataframe of call counts by day
    
    Attributes
    -----------
    None
    """

    def __init__(self):
        """The constructor for FeaturizeCalls class.

        Parameters
        -----------
        None
        """

        self.X = None
        self.y = None

    def fit(self, X, y=None):
        """Fit the call counts by day dataframe to be transformed into a dataframe with date features.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms dataframe into a dataframe with date features.
        

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """

        df = self.X.copy()
        num_days = (
            int(
                np.timedelta64((max(df["date"]) - min(df["date"])), "D")
                / np.timedelta64(1, "D")
            )
            + 1
        )
        start = pd.to_datetime(min(df["date"]))
        dates = [(start + np.timedelta64(i, "D")) for i in range(num_days)]

        seq = pd.DataFrame({"dt_time": dates, "day_seq": np.arange(num_days)})
        seq["date"] = seq["dt_time"].dt.date

        df1 = df.join(seq.set_index("date"), on="date")

        df1["year"] = df1["dt_time"].dt.year
        df1["month"] = df1["dt_time"].dt.month
        df1["day"] = df1["dt_time"].dt.day
        df1["day_of_week"] = df1["dt_time"].dt.weekday
        df1["month_day"] = df1["dt_time"].dt.strftime("%m/%d")
        df1["month_weekday"] = df1["dt_time"].dt.strftime("%b_%a")
        df1["month"] = df1["dt_time"].dt.strftime("%m/%d")
        return df1


class DateDummies:
    """Creates dummy variables of date features.
    
    Attributes
    -----------
    None
    """
    def __init__(self):
        """The constructor for DateDummies class.

        Parameters
        -----------
        None
        """

        self.X = None
        self.y = None

    def fit(self, X, y=None):
        """Fit the call counts by day dataframe to be transformed into a dataframe with date dummy variables.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        # X is the featurized calls dataframe
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms dataframe into a dataframe with dummy variables for date features.
        
        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """

        day_features = [
            "01/06",
            "01/14",
            "02/02",
            "02/07",
            "03/01",
            "03/10",
            "03/20",
            "03/26",
            "04/01",
            "04/08",
            "04/17",
            "04/18",
            "05/06",
            "05/09",
            "05/10",
            "05/21",
            "05/31",
            "06/04",
            "06/05",
            "06/13",
            "06/28",
            "06/30",
            "07/09",
            "07/16",
            "07/20",
            "07/23",
            "07/29",
            "08/01",
            "08/20",
            "08/24",
            "08/28",
            "09/08",
            "09/11",
            "09/14",
            "09/30",
            "10/02",
            "10/17",
            "10/26",
            "11/01",
            "11/15",
            "11/16",
            "11/23",
            "11/27",
            "12/04",
            "12/12",
            "12/19",
            "12/21",
            "12/23",
            "12/29",
        ]
        spec_days = pd.DataFrame({"month_day": day_features, "spec_day": day_features})
        df = self.X.join(spec_days.set_index("month_day"), on="month_day")

        date_dummies = (
            pd.get_dummies(
                df[["date", "day", "month_weekday", "spec_day"]].set_index("date"),
                columns=["day", "month_weekday", "spec_day"],
            )
            .reset_index()
            .drop_duplicates()
        )
        return df.join(date_dummies.set_index("date"), on="date").fillna(0)


class HolidayDummies:
    """Creates dummy variables of holiday features.
    
    Attributes
    -----------
    None
    """
    def __init__(self):
        """The constructor for HolidayDummies class.

        Parameters
        -----------
        None
        """
        self.X = None
        self.y = None

    def fit(self, X, y=None):
        """Fit the call counts by day dataframe to be transformed into a dataframe with holiday dummy variables.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        # X is a dictionary of Holidays
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms dataframe into a dataframe with dummy variables for holiday features.
        
        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """
        _holidays = []
        for date in sorted(self.X.keys()):
            _holidays.append([date, self.X[date]])
        _holidays = pd.DataFrame(_holidays, columns=["date", "holiday"])
        return pd.get_dummies(_holidays.set_index("date")).reset_index()


class EventDummies:
    """Creates dummy variables of holiday features.
    
    Attributes
    -----------
    event_dict: Dictionary of local events in Seattle {keys= str of event names, values=string of dates for event}
    """

    def __init__(self, event_dict=None):
        """The constructor for EventDummies class.

        Parameters
        -----------
        event_dict: Dictionary of local events in Seattle {keys= str of event names, values=string of dates for event}
        """
        self.X = None
        self.y = None
        self.event_dict = event_dict

        defualt_events = {
            "Pride Parade": [
                "6/30/2019",
                "6/24/2018",
                "6/25/2017",
                "6/26/2016",
                "6/28/2015",
                "6/29/2014",
                "6/30/2013",
                "6/24/2012",
                "6/26/2011",
                "6/27/2010",
            ],
            "Seafair": [
                "8/2/2019",
                "8/3/2019",
                "8/4/2019",
                "8/3/2018",
                "8/4/2018",
                "8/5/2018",
                "8/4/2017",
                "8/5/2017",
                "8/6/2017",
                "8/5/2016",
                "8/6/2016",
                "8/7/2016",
                "7/31/2015",
                "8/1/2015",
                "8/2/2015",
                "8/1/2014",
                "8/2/2014",
                "8/3/2014",
                "8/2/2013",
                "8/3/2013",
                "8/4/2013",
                "8/3/2012",
                "8/4/2012",
                "8/5/2012",
                "8/5/2011",
                "8/6/2011",
                "8/7/2011",
                "8/6/2010",
                "8/7/2010",
                "8/8/2010",
            ],
            "Soltice Parade": [
                "6/30/2019",
                "6/16/2018",
                "6/17/2017",
                "6/18/2016",
                "6/20/2015",
                "6/21/2014",
                "6/22/2013",
                "6/16/2012",
                "6/18/2011",
                "6/19/2010",
            ],
            "Womens March": ["1/19/2019", "1/20/2018", "1/21/2017"],
        }

        if self.event_dict == None:
            self.event_dict = defualt_events

    def fit(self, X=None, y=None):
        """Fit the call counts by day dataframe to be transformed into a dataframe with event dummy variables.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms dataframe into a dataframe with dummy variables for event features.
        
        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """
        _events = []
        for event in self.event_dict.keys():
            for day in self.event_dict[event]:
                _events.append([dt.datetime.strptime(day, "%m/%d/%Y"), event])

        _events = pd.DataFrame(_events, columns=["date", "local_event"])
        _events["date"] = _events["date"].dt.date
        return pd.get_dummies(_events.set_index("date")).reset_index()


class MakeDummies:
    """Creates dummy variables.
    
    Attributes
    -----------
    None
    """
    def __init__(self):
        """The constructor for MakeDummies class.

        Parameters
        -----------
        None
        """
        self.X = None
        self.y = None

    def fit(self, X, y=None):
        """Fit the call counts by day dataframe to be transformed into a dataframe with additional dummy variables.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms dataframe into a dataframe with additional dummy.
        
        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """
        return pd.get_dummies(self.X.set_index("date")).reset_index()


class MakeModelInput:
    """Creates data frame with all features to be used in running models.
    
    Attributes
    -----------
    None
    """
    def __init__(self):
        """The constructor for MakeModelInput class.

        Parameters
        -----------
        None
        """
        self.X = None
        self.y = None

    def fit(self, X, y=None):
        """Fit the call counts by day dataframe to be transformed into a dataframe of features for input into models.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        # X is the calls dataframe
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms dataframe into a dataframe of features for input into models.
        
        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """
        retriever = DataRetrieval()
        weather = retriever.get_weather_data()
        seahawks_schedule = retriever.get_seahawks_schedule()
        huskies_schedule = retriever.get_huskies_schedule()
        sounders_schedule = retriever.get_sounders_schedule()
        sports = MakeDummies()
        sports.fit(seahawks_schedule)
        seahawks = sports.transform()
        sports.fit(huskies_schedule)
        huskies = sports.transform()
        sports.fit(sounders_schedule)
        sounders = sports.transform()
        us_holiday_dict = SeattleHolidays.CustomHolidays()
        us_holiday_dict._populate()
        holidayier = HolidayDummies()
        holidayier.fit(us_holiday_dict)
        us_holidays = holidayier.transform()
        jewish_holiday_dict = SeattleHolidays.JewishHolidays()
        jewish_holiday_dict._populate()
        holidayier.fit(jewish_holiday_dict)
        jewish_holidays = holidayier.transform()
        islamic_holiday_dict = SeattleHolidays.IslamicHolidays()
        islamic_holiday_dict._populate()
        holidayier.fit(islamic_holiday_dict)
        islamic_holidays = holidayier.transform()
        event_dummies = EventDummies()
        event_dummies.fit()
        events = event_dummies.transform()
        joiner = JoinDataFrames(
            weather,
            us_holidays,
            islamic_holidays,
            jewish_holidays,
            events,
            seahawks,
            huskies,
            sounders,
        )
        joiner.fit(self.X)
        return joiner.transform()


class JoinDataFrames:
    """Creates data of all data.
    
    Attributes
    -----------
    weather: Dataframe of weather features
    us_holidays: Dataframe of US Christian and Secular holiday dummy variables
    islamic_holidays: Dataframe of Islamic holiday dummy variables
    jewish_holidays: Dataframe of Jewish holiday dummy variables
    events: Dataframe of dummy variables for local events
    seahawks: Dataframe of dummy variables for Seahawks football games
    huskies: Dataframe of dummy variables for University of Washington Huskies football games
    sounders: Dataframe of dummy variables for Sounders FC soccer matches
    """
    def __init__(
        self,
        weather,
        us_holidays,
        islamic_holidays,
        jewish_holidays,
        events,
        seahawks,
        huskies,
        sounders,
    ):
        """The constructor for JoinDataFrames class.

        Parameters
        -----------
        weather: Dataframe of weather features
        us_holidays: Dataframe of US Christian and Secular holiday dummy variables
        islamic_holidays: Dataframe of Islamic holiday dummy variables
        jewish_holidays: Dataframe of Jewish holiday dummy variables
        events: Dataframe of dummy variables for local events
        seahawks: Dataframe of dummy variables for Seahawks football games
        huskies: Dataframe of dummy variables for University of Washington Huskies football games
        sounders: Dataframe of dummy variables for Sounders FC soccer matches
        """
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
        """Fit the call counts by day dataframe to be combined with features to be used in models.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms dataframe into a dataframe with combined calls for service data and features.
        
        Parameters
        -----------
        X: dataframe

        Returns
        --------
        dataframe
        """
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
        """Function used by the transform method to join dataframes together.
        
        Parameters
        -----------
        df1: dataframe
        df2: dataframe

        Returns
        --------
        dataframe
        """
        return df1.join(df2.set_index("date"), on="date")


class FeaturizeDates:
    """Creates dataframe of dates and date features to be used in generating forecast.
    
    Attributes
    -----------
    start_date: string of the start date ('mm/dd/yyyy')
    end_date: string of the end date ('mm/dd/yyyy')
    model_end: tuple (string of the last date ('mm/dd/yyyy')used in model, integer of the last day sequence used in model)
    """

    def __init__(self, start_date, end_date, model_end):
        """The constructor for JoinDataFrames class.

        Parameters
        -----------
        start_date: string of the start date ('mm/dd/yyyy')
        end_date: string of the end date ('mm/dd/yyyy')
        model_end: tuple (string of the last date ('mm/dd/yyyy')used in model, integer of the last day sequence used in model)
        """
        self.start_date = start_date
        self.end_date = end_date
        self.model_end = model_end
        self.X = None
        self.y = None

    def fit(self, X=None, y=None):
        """Fits date information to be transormed into dataframe of dates with date features.

        Parameters
        -----------
        X: None

        Returns
        --------
        self
        """
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms date information into a dataframe of dates and date features.
        
        Parameters
        -----------
        X: None

        Returns
        --------
        dataframe
        """
        num_days = (
            int(
                np.timedelta64(
                    pd.to_datetime(self.end_date) - pd.to_datetime(self.start_date), "D"
                )
                / np.timedelta64(1, "D")
            )
            + 1
        )
        dates = [
            (pd.to_datetime(self.start_date) + np.timedelta64(i, "D"))
            for i in range(num_days)
        ]
        start_seq = int(
            (
                np.timedelta64(
                    pd.to_datetime(self.start_date) - pd.to_datetime(self.model_end[0]),
                    "D",
                )
                + self.model_end[1]
            )
            / np.timedelta64(1, "D")
        )
        df = pd.DataFrame(
            {"dt_time": dates, "day_seq": np.arange(start_seq, start_seq + num_days)}
        )
        df["date"] = df["dt_time"].dt.date
        df["year"] = df["dt_time"].dt.year
        df["month"] = df["dt_time"].dt.month
        df["day"] = df["dt_time"].dt.day
        df["day_of_week"] = df["dt_time"].dt.weekday
        df["month_day"] = df["dt_time"].dt.strftime("%m/%d")
        df["month_weekday"] = df["dt_time"].dt.strftime("%b_%a")
        return df


class AddWeatherForecast:
    """Adds weather forecast data to dataframe of dates and date features to use in forecast.
    
    Attributes
    -----------
    None
    """
    def __init__(self):
        """The constructor for AddWeatherForecast class.

        Parameters
        -----------
        None
        """
        self.X = None
        self.y = None

    def fit(self, X, y=None):
        """Fits forecast dates dataframe to be transormed into dataframe of dates with date features.

        Parameters
        -----------
        X: dataframe

        Returns
        --------
        self
        """
        # X is a dataframe of dates with date features
        self.X = X
        self.y = y
        return self

    def transform(self, y=None):
        """Transforms date information into a dataframe of dates with weather forecast data.
        
        Parameters
        -----------
        X: None

        Returns
        --------
        dataframe
        """
        forecast_dates = self.X[["dt_time", "month_day"]]
        weather_avg = pd.read_csv("../data/weather_averages.csv")
        weather_fcst = weather_avg[
            ["DATE", "DLY-TMAX-NORMAL", "DLY-PRCP-50PCTL", "DLY-SNOW-50PCTL"]
        ]
        weather_fcst["DATE"] = pd.to_datetime(
            weather_fcst["DATE"].astype("str"), format="%Y%m%d", errors="ignore"
        )
        weather_fcst["month_day"] = weather_fcst["DATE"].dt.strftime("%m/%d")
        weather_fcst = weather_fcst[
            ["month_day", "DLY-PRCP-50PCTL", "DLY-TMAX-NORMAL", "DLY-SNOW-50PCTL"]
        ].rename(
            columns={
                "DLY-PRCP-50PCTL": "precip",
                "DLY-TMAX-NORMAL": "temp_max",
                "DLY-SNOW-50PCTL": "snow",
            }
        )
        weather_fcst["snow"] = 0.0
        weather_fcst = forecast_dates.join(
            weather_fcst.set_index("month_day"), on="month_day"
        )
        near_term_weather = seattle_weather_fcst()

        for i in range(len(near_term_weather)):
            weather_fcst["temp_max"][
                weather_fcst["dt_time"] == near_term_weather["date"][i]
            ] = near_term_weather["temp_max"][i]
            if near_term_weather["precip_bool"][i] == 0:
                weather_fcst["precip"][
                    weather_fcst["dt_time"] == near_term_weather["date"][0]
                ] = 0

        self.X[["precip", "temp_max", "snow"]] = weather_fcst[
            ["precip", "temp_max", "snow"]
        ]
        return self.X.drop(
            columns=[
                "dt_time",
                "year",
                "month",
                "day",
                "day_of_week",
                "month_day",
                "month_weekday",
                "spec_day",
            ]
        )

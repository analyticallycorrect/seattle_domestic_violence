import pandas as pd
import numpy as np

from src.sports_scrapers import scrape_huskies, scrape_seahawks
from src.weather_scraper import (
    get_raw_forecast,
    get_raw_forecast_dataframe,
    get_hi_temperature,
    seattle_weather_fcst,
)
from src.data_retrievers import DataRetrieval
from src.holiday_calendars import SeattleHolidays
from src.featurizers import (
    CountCalls,
    FeaturizeCalls,
    DateDummies,
    HolidayDummies,
    EventDummies,
    MakeDummies,
    JoinDataFrames,
    MakeModelInput,
    FeaturizeDates,
    AddWeatherForecast,
)

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


def calls_pipe(calls_df):
    calls_pipe = Pipeline(
        steps=[
            ("counter", CountCalls(how="neighborhood")),
            ("feturizer", FeaturizeCalls()),
            ("date_dummifier", DateDummies()),
            ("model_input", MakeModelInput()),
        ]
    )
    calls_pipe.fit(calls_df)
    calls_neighborhood = calls_pipe.transform(calls_df)
    targets = calls_neighborhood.pivot_table(
        values="num_calls", index="date", columns="neighborhood"
    )
    features = calls_neighborhood.drop(
        columns=[
            "neighborhood",
            "date",
            "num_calls",
            "dt_time",
            "year",
            "month",
            "day",
            "day_of_week",
            "month_day",
            "month_weekday",
            "spec_day",
        ]
    ).drop_duplicates()
    return targets, features


def forecast_pipe(start_date, end_date, model_end):
    forecast_pipe = Pipeline(
        steps=[
            ('date_featurizer', FeaturizeDates(start_date, end_date, model_end)),
            ('date_dummifier', DateDummies()),
            ('model_input', MakeModelInput()),
            ('add_weather', AddWeatherForecast()),
        ]
    )
    forecast_pipe.fit(None)
    forecast_features = forecast_pipe.transform(None)
    return forecast_features


def baseline_model(X_train, y_train):
    neighborhood_model = LinearRegression()
    neighborhood_model.fit(X_train, y_train)
    return neighborhood_model


def city_model(X_train, y_train):
    model_city = GradientBoostingRegressor(
        n_estimators=752, learning_rate=0.01, max_depth=3, subsample=0.6
    )
    model_city.fit(X_train, y_train.sum(axis=1))
    return city_model


def neighborhood_dist_model(X_train, y_train):
    neighborhood_dist_train = pd.DataFrame(
        np.array(y_train.T) / np.array(y_train.sum(axis=1))
    ).T
    rf_dist = RandomForestRegressor(
        n_estimators=10000,
        min_samples_split=5,
        min_samples_leaf=1,
        max_features="auto",
        max_depth=10,
        bootstrap=True,
    )
    rf_dist.fit(X_train, neighborhood_dist_train)
    return rf_dist


def model_ensemble(city_counts, neighborhood_dist):
    return city_counts * neighborhood_dist.T

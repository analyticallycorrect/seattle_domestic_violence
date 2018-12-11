import pandas as pd
import numpy as np


def neighborhood_ratings(predictions_df, features, column_names):
    neighborhood_predicted_counts  = predictions_df.T
    neighborhood_predicted_counts.columns = column_names
    neighborhood_predicted_counts = neighborhood_predicted_counts.join(features['date'])
    neighborhood_means = neighborhood_predicted_counts.mean()
    neighborhood_std = neighborhood_predicted_counts.std()
    ratings = (((neighborhood_means - neighborhood_predicted_counts.drop('date', axis=1)) / (neighborhood_std*2)) + .5)
    ratings = ratings.join(features['date'])
    return ratings
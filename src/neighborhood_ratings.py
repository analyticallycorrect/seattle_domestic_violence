import pandas as pd
import nump as np


def neighborhood_ratings(predictions_df, column_names):
    neighborhood_predicted_counts = pd.DataFrame(predictions_df.T, columns=column_names)
    neighborhood_means = neighborhood_predicted_counts.mean()
    neighborhood_std = neighborhood_predicted_counts.std()
    ratings = (((neighborhood_means - neighborhood_predicted_counts.drop('date', axis=1)) / (neighborhood_std*2)) + .5)
    return ratings
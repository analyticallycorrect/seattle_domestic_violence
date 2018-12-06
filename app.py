import numpy as np
import pandas as pd
from io import BytesIO
import folium 

from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_url_path="")

#csv files with forecast data and ratings for heatmap
city_predictions = pd.read_csv('data/city_predictions.csv')
neighborhood_ratings = pd.read_csv('data/neighborhood_ratings.csv')
neighborhood_predictions = pd.read_csv('data/neighborhood_predictions.csv')


@app.route('/') #landing page
def settle_dv():
    return render_template('index.html')
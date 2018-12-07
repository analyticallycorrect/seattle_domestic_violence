import numpy as np
import pandas as pd
import datetime as dt
from io import BytesIO
import folium 
from folium import GeoJson
import shapefile
import branca.colormap as cm
import json

from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_url_path="")

#csv files with forecast data and ratings for heatmap
city_predictions = pd.read_csv('data/city_predictions.csv')
neighborhood_ratings = pd.read_csv('data/neighborhood_ratings.csv')
neighborhood_predictions = pd.read_csv('data/neighborhood_predictions.csv')

with open('data/seattle_neighborhood_shapes.geojson') as f:
    mcpp_neighoborhoods = json.load(f)


@app.route('/') #landing page
def settle_dv():
    return render_template('index.html')


@app.route('/query/<date_idx>', methods=['GET'])
def query_date(date_idx):
    date_idx = int(date_idx)
    mapping = map_seattle(date_idx)
    i_frame = '<iframe src="/map/' + str(date_idx) + '" width="100%" height="595"> </iframe>'
    return render_template('index.html', map=i_frame)
    

@app.route('/map/<date_idx>', methods=['GET'])
def map(date_idx):
    date_idx = int(date_idx)
    return map_seattle(date_idx)

def my_color_function(feature, date_idx):
    """Maps low values to green and hugh values to red."""
    try:
        rating = neighborhood_ratings.iloc[date_idx][feature['properties']['name']]
        return rating
    except KeyError:
        return 0.5

def map_seattle(date_idx):
    linear = cm.linear.RdYlGn_06
    seattle_neighborhoods = folium.Map(location=[47.61, -122.3321],
                                       zoom_start=11,tiles='cartodbpositron')
    
    GeoJson(mcpp_neighoborhoods,
        style_function=lambda feature: {
        'fillColor': linear(my_color_function(feature, date_idx)),
        'fillOpacity': 0.45,
        'color': 'gray',
        'dashArray': '5, 5'}).add_to(seattle_neighborhoods)
    
    mapdata = BytesIO()
    seattle_neighborhoods.save(mapdata, close_file=False)
    html = mapdata.getvalue()
    return html
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
city_predictions = pd.read_pickle('dashboard_data/city_predictions.pkl')
neighborhood_ratings = pd.read_pickle('dashboard_data/neighborhood_ratings.pkl')
neighborhood_predictions = pd.read_pickle('dashboard_data/neighborhood_predictions.pkl')

with open('dashboard_data/seattle_neighborhood_shapes.geojson') as f:
    mcpp_neighoborhoods = json.load(f)


@app.route('/') #landing page
def settle_dv():
    today = dt.date.today().strftime("%m/%d/%Y")
    date_idx = (int((pd.to_datetime(neighborhood_ratings['date'])[pd.to_datetime(neighborhood_ratings['date'])==pd.to_datetime(today)].index).values))
    mapping = map_seattle(date_idx)
    i_frame = '<iframe src="/map/' + str(date_idx) + '" width="100%" height="595"> </iframe>'
    return render_template('index.html', map=i_frame, table=render_table(today), date=today)


@app.route('/<date_str>', methods=['GET'])
def query_date(date_str):
    date_str = date_str.replace('-', '/')
    date_idx = (int((pd.to_datetime(neighborhood_ratings['date'])[pd.to_datetime(neighborhood_ratings['date'])==pd.to_datetime(date_str)].index).values))
    mapping = map_seattle(date_idx)
    i_frame = '<iframe src="/map/' + str(date_idx) + '" width="100%" height="595"> </iframe>'
    return render_template('index.html', map=i_frame, table=render_table(date_str), date=date_str)
    

@app.route('/map/<date_idx>', methods=['GET'])
def map(date_idx):
    date_idx = int(date_idx)
    return map_seattle(date_idx)

def render_table(date_str):
    date_idx = (int((pd.to_datetime(neighborhood_ratings['date'])[pd.to_datetime(neighborhood_ratings['date'])==pd.to_datetime(date_str)].index).values))
    predictions = pd.concat([pd.DataFrame(neighborhood_predictions.iloc[date_idx]), neighborhood_predictions.mean()], axis=1).drop(labels='date').reset_index()
    predictions.columns = ["neighborhood", "predicted_rate", "average_rate"]
    output = []
    for i in range(len(predictions)):
        row = predictions.iloc[i]
        output.append({'neighborhood' : row['neighborhood'],
                    'predicted_rate' : row['predicted_rate'].round(decimals=2), 'average_rate': row['average_rate'].round(decimals=2)})
    """populate table to display"""
    table = render_template('table.html', rows = output)
    return table

def my_color_function(feature, date_idx):
    """Maps low values to green and hugh values to red."""
    try:
        rating = neighborhood_ratings.iloc[date_idx][feature['properties']['name']]
        return rating
    except KeyError:
        return 0.5

def map_seattle(date_idx):
    date_idx = int(date_idx)
    linear = cm.linear.RdYlGn_06
    seattle_neighborhoods = folium.Map(location=[47.61, -122.3321],
                                       zoom_start=11,tiles='cartodbpositron')
    
    GeoJson(mcpp_neighoborhoods,
        style_function=lambda feature: {
        'fillColor': linear(my_color_function(feature, date_idx)),
        'fillOpacity': 0.45,
        'color': 'gray',
        'dashArray': '2, 5'}).add_to(seattle_neighborhoods)
    
    mapdata = BytesIO()
    seattle_neighborhoods.save(mapdata, close_file=False)
    html = mapdata.getvalue()
    return html
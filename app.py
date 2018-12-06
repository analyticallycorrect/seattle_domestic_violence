import numpy as np
import pandas as pd
from Filter_Data import Run_Recommender
from Group_Runs import GroupRuns
import Mapping_Functions.Map_Routes as mapfun
from io import BytesIO
import folium 

from flask import Flask, request, render_template, jsonify
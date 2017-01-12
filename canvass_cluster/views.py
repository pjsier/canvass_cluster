from __future__ import absolute_import, print_function, unicode_literals

from flask import Blueprint, render_template, request, current_app
from canvass_cluster.cluster import ClusterCreator
import requests
import numpy as np
import json
import os

views = Blueprint('views', __name__)


def mapzen_matrix(locs):
    mapzen_locs = {
        'locations': [{'lat': p['lat'], 'lon': p['lon']} for p in locs],
        'costing': 'auto'
    }
    mapzen_url = 'http://matrix.mapzen.com/many_to_many?json={}&api_key={}'.format(
        json.dumps(mapzen_locs),
        current_app.config['MAPZEN_KEY']
    )

    r = requests.get(mapzen_url).json()
    matrix_dist = []
    for m in r['many_to_many']:
        matrix_dist.append([p['time'] for p in m])

    return matrix_dist


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/locations', methods=['POST'])
def handle_locations():
    locs = request.json['locations']
    matrix = None
    # Use mapzen distances if less than 50 points
    if len(locs) <= 50:
        matrix = mapzen_matrix(locs)
    cluster_handler = ClusterCreator(locs, matrix=matrix)
    clusters = request.json.get('clusters', None)
    num_clusters = clusters if clusters is not None else 20

    return json.dumps({'locations': cluster_handler(num_clusters=num_clusters)})

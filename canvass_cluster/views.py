from __future__ import absolute_import, print_function, unicode_literals

from flask import Blueprint, render_template, request
from canvass_cluster.cluster import ClusterCreator
import requests
import numpy as np
import json
import os

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/locations', methods=['POST'])
def handle_locations():
    locs = request.json['locations']
    num_clusters = request.json.get('clusters', None)
    if not num_clusters:
        num_clusters = 20
    
    cluster_handler = ClusterCreator(locs, num_clusters)

    return json.dumps({'locations': cluster_handler()})

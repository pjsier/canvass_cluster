from __future__ import absolute_import, print_function, unicode_literals

from flask import Blueprint, render_template, request
from canvass_cluster.cluster import ClusterCreator
import requests
import json
import os

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/locations', methods=['POST'])
def handle_locations():
    cluster_handler = ClusterCreator(request.json['locations'])
    clusters = request.json.get('clusters', None)
    num_clusters = clusters if clusters is not None else 20

    return json.dumps({'locations': cluster_handler(num_clusters=num_clusters)})

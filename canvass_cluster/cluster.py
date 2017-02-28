from __future__ import absolute_import, print_function, unicode_literals

from hcluster import pdist, squareform, linkage, fcluster
from math import radians, cos, sin, asin, sqrt
import numpy as np
import requests
import json


def haversine(p1, p2):
    # convert decimal degrees to radians
    lat1 = p1[0]
    lon1 = p1[1]
    lat2 = p2[0]
    lon2 = p2[1]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6372.795 * c

    return km


class ClusterCreator(object):
    """
    Takes in a list of location dicts, calculates the distance between the points,
    and assigns clustered groups adding it as a key, value pair in each dict
    """
    def __init__(self, locations, num_clusters, api_key):
        self.locations = locations
        self.num_clusters = num_clusters
        self.api_key = api_key

        if len(self.locations) <= 50:
            self.point_arr = self.mapzen_matrix(
                [{'lat': p['lat'], 'lon': p['lon']} for p in self.locations]
            )
        else:
            self.point_arr = self.time_subcluster(
                np.array([[p['lon'], p['lat']] for p in self.locations])
            )

    def __call__(self):
        # Can continue to play around with these
        self.cluster_linkage = linkage(self.point_arr, method='ward')
        self.clusters = fcluster(self.cluster_linkage,
                                 self.num_clusters,
                                 criterion='maxclust')

        [p[0].update({'group': p[1]}) for p in zip(self.locations, self.clusters.tolist())]

        return self.locations

    def mapzen_matrix(self, locs):
        mapzen_locs = {
            'locations': locs,
            'costing': 'auto'
        }
        mapzen_url = 'http://matrix.mapzen.com/many_to_many?json={}&api_key={}'.format(
            json.dumps(mapzen_locs),
            self.api_key
        )

        r = requests.get(mapzen_url).json()
        matrix_dist = []
        for m in r['many_to_many']:
            matrix_dist.append([p['distance'] for p in m])

        return np.array(matrix_dist, dtype=float)

    def time_subcluster(self, locs):
        # Getting subclusters at Mapzen's limit
        cluster_linkage = linkage(locs, method='ward')
        clusters = fcluster(cluster_linkage, 50, criterion='maxclust')

        cluster_means = np.array([np.mean(
            locs[np.where(clusters == i)], axis=0
        ) for i in range(1, 51)])

        mapzen_locs = [{'lat': p[1], 'lon': p[0]} for p in cluster_means]
        mapzen_matrix = self.mapzen_matrix(mapzen_locs)

        # Cluster labels used for mapping back together
        # Subtracting one to use 0 index
        cl = clusters - 1

        # Get a matching distance matrix of lat/lon distance, get ratios
        cluster_km_dist = squareform(pdist(cluster_means,
                                           (lambda u,v: haversine(u,v))))

        dist_ratio_matrix = np.nan_to_num(np.divide(mapzen_matrix,
                                                    cluster_km_dist))
        # Divide items by mean to normalize a bit
        dist_ratio_matrix = np.nan_to_num(np.divide(dist_ratio_matrix,
                                                    dist_ratio_matrix.mean()))

        locs_km_dist = squareform(pdist(locs, (lambda u,v: haversine(u,v))))

        # Iterate through each, updating by ratio in dist_ratio_matrix
        it = np.nditer(locs_km_dist, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            it[0] = it[0] * dist_ratio_matrix[cl[it.multi_index[0]]][cl[it.multi_index[1]]]
            it.iternext()

        return locs_km_dist

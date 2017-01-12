from __future__ import absolute_import, print_function, unicode_literals

from scipy.cluster.hierarchy import linkage, fcluster
import numpy as np
import json


class ClusterCreator:
    """
    Takes in a list of location dicts, calculates the distance between the points,
    and assigns clustered groups adding it as a key, value pair in each dict
    """
    def __init__(self, locations, matrix=None):
        self.locations = locations
        if matrix is not None:
            self.point_arr = np.array(matrix)
        else:
            self.point_arr = np.array([[p['lon'], p['lat']] for p in self.locations])

    def __call__(self, num_clusters=20):
        # Can continue to play around with these
        self.cluster_linkage = linkage(self.point_arr, method='ward')
        self.clusters = fcluster(self.cluster_linkage,
                                 num_clusters,
                                 criterion='maxclust')

        [p[0].update({'group': p[1]}) for p in zip(self.locations, self.clusters.tolist())]

        return self.locations

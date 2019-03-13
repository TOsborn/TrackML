########################################################################
# ======================  TrackML CHALLENGE MODEL  =====================
########################################################################
# Author: Isabelle Guyon, Victor Estrade
# Date: Apr 10, 2018

# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS".
# PARIS-SUD UNIVERSITY, THE ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRIGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS.
# IN NO EVENT SHALL PARIS-SUD UNIVERSITY AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL,
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS,
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE.

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

__authors__ = ['Sabrina Amrouche', 'David Rousseau', 'Moritz Kiehn', 'Ilija Vukotic']


class Model():
    def __init__(self, eps=0.008, min_samples=1, metric='euclidean',
                 algorithm='kd_tree', leaf_size=30, p=None, n_jobs=1, verbose=1):
        super().__init__()
        self.dbscan = DBSCAN(eps=eps, min_samples=min_samples,
                             metric=metric, algorithm=algorithm,
                             leaf_size=leaf_size, p=p, n_jobs=n_jobs)
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.n_jobs = n_jobs
        self.verbose = verbose

    def _preprocess(self, hits):
        x = hits.x.values
        y = hits.y.values
        z = hits.z.values

        r = np.sqrt(x**2 + y**2 + z**2)
        hits['x2'] = x / r
        hits['y2'] = y / r

        r = np.sqrt(x**2 + y**2)
        hits['z2'] = z / r

        ss = StandardScaler()
        X = ss.fit_transform(hits[['x2', 'y2', 'z2']].values)

        return X

    def predict_one_event(self, event_id, event, cells=None):
        X = self._preprocess(event.copy())
        labels = self.dbscan.fit_predict(X)

        sub = pd.DataFrame(data=np.column_stack((event.hit_id.values, labels)),
                           columns=["hit_id", "track_id"]).astype(int)
        sub['event_id'] = event_id
        return sub

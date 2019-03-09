import sys

import numpy as np
import pandas as pd

trackml_path = '/home/ec2-user/SageMaker/TrackML'
if trackml_path not in sys.path:
    sys.path.append(trackml_path)
    
from helper_functions.file_utilities import file_url


def bin_id(R, theta, z, grid_boundaries):
    R_bin = np.digitize(R, grid_boundaries.R).item()
    theta_bin = np.digitize(theta, grid_boundaries.theta).item()
    z_bin = np.digitize(z, grid_boundaries.z).item()
    
    return R_bin, theta_bin, z_bin


def write_boundaries_csv(event_ids, q_list):
    hits = prep_hits(event_ids)
    for q in q_list:
        R_bounds, theta_bounds, z_bounds = make_grid_boundaries(hits, q)
        
        R_bounds.to_csv(
            '/home/ec2-user/SageMaker/efs/grid_boundary_arrays/R_bounds-{}.csv'.format(q),
            index=False
        )
        theta_bounds.to_csv(
            '/home/ec2-user/SageMaker/efs/grid_boundary_arrays/theta_bounds-{}.csv'.format(q),
            index=False
        )
        z_bounds.to_csv(
            '/home/ec2-user/SageMaker/efs/grid_boundary_arrays/z_bounds-{}.csv'.format(q),
            index=False
        )
    
def make_grid_boundaries(hits, q):
    _, R_bounds = pd.qcut(
        hits.R,
        q,
        duplicates='drop',
        retbins=True
    )
    _, z_bounds = pd.qcut(
        hits.z,
        q,
        duplicates='drop',
        retbins=True
    )
    
    theta_bounds = np.linspace(-np.pi, np.pi, q+1, endpoint=False)
    
    print('q', q)
    print('R_bounds', len(R_bounds))
    print('z_bounds', len(z_bounds))
    print('theta_bounds', len(theta_bounds))
    print()
        
    return pd.Series(R_bounds), pd.Series(theta_bounds), pd.Series(z_bounds)


def prep_hits(event_ids):
    return pd.concat(prep_event_hits(eid) for eid in event_ids)


def prep_event_hits(event_id):
    hits = pd.read_csv(file_url('hits', event_id))
    
    hits['R'] = np.sqrt(np.square(hits.x) + np.square(hits.y))
    hits['theta'] = np.arctan2(hits.x, hits.y)
    
    return hits.drop([
        'hit_id',
        'volume_id',
        'layer_id',
        'module_id',
        'x',
        'y',
    ], axis=1).reindex(columns=[
        'R',
        'theta',
        'z'
    ])

    
    

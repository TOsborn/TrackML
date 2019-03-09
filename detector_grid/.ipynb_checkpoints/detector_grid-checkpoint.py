import sys

import numpy as np
import pandas as pd

trackml_path = '/home/ec2-user/SageMaker/TrackML'
if trackml_path not in sys.path:
    sys.path.append(trackml_path)

class DetectorGrid:
    """Class for dividing the detector region into bins.
    
    The detector region is partitioned by three types of boundary
    surfaces:
        1.  R-boundaries: Concentric cylinders centered on the z-axis.
            
        2.  theta-boundaries: Planes containing the z-axis spaced by
            equal angles.
            
        3.  z-boundaries: Planes perpendicular to the z-axis.
        
    The R and z-boundaries are created by binning into buckets of equal
    count based on sample quantiles. Repeated values for these parameters
    are counted only once, which helps to avoid problems caused by the
    detectors having different orientations. theta-boundaries are divided
    into evenly spaced bins rather than ones having equal sample counts.
            
    This approach results in bins which are relatively compact, invariant
    with rotation about the z-axis, and whose volume scales with their
    distance from the origin. It also allows for partitioning bins into
    equivalence classes of equal size, where R and z are equal for all
    bins in a class but theta is allowed to vary. This is important for
    our application.
            
    """
    def __init__(self, q):
        self.grid_boundaries = pd.read_csv('/home/ec2-user/SageMaker/efs/detector_bin_arrays/grid_boundaries.csv') # -{}.csv'.format(q))
        
        
    def add_bin_cols(self, hits):
        hits['R_bin'] = np.digitize(hits.R, self.grid_boundaries.R)
        hits['theta_bin'] = np.digitize(hits.theta, self.grid_boundaries.theta)
        hits['z_bin'] = np.digitize(hits.z, self.grid_boundaries.z)
        
        
    
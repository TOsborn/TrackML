import sys
import numpy as np

trackml_path = '/home/ec2-user/SageMaker/TrackML'
if trackml_path not in sys.path:
    sys.path.append(trackml_path)

class DetectorGrid:
    """Class for dividing the detector region into bins.
    
    The detector region is partitioned by three types of boundary
    surfaces:
        1.  Concentric cylinders centered on the z-axis whose radii
            increase quadratically. Their number is specified by the
            parameter R_bins.
            
        2.  Planes containing the z-axis spaced by equal rotations.
            Their number is specified by theta_bins.
            
        3.  Planes perpendicular to the z-axis whose distance from
            the plane z = 0 increases quadratically. The number of
            planes on each side of the plane z = 0 is specified by
            z_bins.
            
    This approach results in bins which are relatively compact, invariant
    with rotation about the z-axis, and whose volume scales with their
    distance from the origin. It also allows for partitioning bins into
    equivalence classes of equal size, where R and z are equal for all
    bins in a class but theta is allowed to vary. This is important for
    our application.
            
    """

    def __init__(self, R_bins, theta_bins, z_bins):
        R_min, R_max = 30. 1030.
        z_min, z_max = 
        
        self.R_grid = np.square(np.linspace(np.sqrt(30.), np.sqrt(1030.), R_res))
        self.cos_grid = np.cos(np.linspace(-np.pi, 0., rot_res))
        self.other_axes = [[1, 2], [0, 2], [0, 1]]

        
    def get_bin_id(self, x, y, z):
        v = np.array([x, y, z])
        partition_idx = v.argmax()
        
        R = np.linalg.norm(v)
        R_idx = np.digitize(R, self.R_grid)
        
        u = v[self.other_axes[partition_idx]] / R
        ang_idx_1, ang_idx_2 = np.digitize(u, self.cos_grid)
        
        return R_idx, partition_idx, ang_idx_1, ang_idx_2
        
        
    
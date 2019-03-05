import sys
import numpy as np

trackml_path = '/home/ec2-user/SageMaker/TrackML'
if trackml_path not in sys.path:
    sys.path.append(trackml_path)

class DetectorGrid:
    """Class for dividing the detector region into bins.
    
    There are two types of boundary surfaces:
        1.  Concentric circles centered at the origin whose radii 
            increase exponentially. Their number is specified by the
            parameter R_res.
            
        2.  Planes containing one of the three axes. The number
            of planes containing each axis is specified by the
            parameter rot_res. For each axis, the planes containing
            it are spaced evenly by rotational angles equal to
            2*pi/rot_res.
    
    The detector region is divided into partitions defined by
    
    P_i = {v in R^3 : argmin(v) == i}.
    
    The points in partition P_i are divided into bins by the planes
    containing the jth axis, where j != i, and the concentric circles
    described above.
    
    This approach results in bins which are relatively compact, have
    volume which is approximately invariant with rotation, and which
    scale on all axes in proportion to their distance from the origin.
    Only bins lying on the boundaries between partitions tend to be
    irregular.
    
    """
    

    def __init__(self, R_res, rot_res):
        self.R_grid = np.linspace(np.sqrt(30.), np.sqrt(1030.), R_res)**2
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
        
        
    
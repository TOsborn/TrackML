# CONSTANTS 
CHILDREN = 0
WEIGHT = 1

import sys
import pandas as pd
from time import time

trackml_path = '/home/ec2-user/SageMaker/TrackML'
if trackml_path not in sys.path:
    sys.path.append(trackml_path)
    
from helper_functions.file_utilities import file_url
    
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

    
def create_segment_dict(event_ids, max_depth=3, get_sizeof_list=False):
    segment_dict = {CHILDREN: {}, WEIGHT: 0}
    sizeof_list = []
    start = last = time()
    for i, eid in enumerate(event_ids):
        add_event_segment_dict(eid, segment_dict, max_depth=max_depth)
        sizeof_list.append(get_size(segment_dict))
        print(str(i+1)+':\n\t', str(time() - last) + '\n\t', sizeof_list[-1])
        last = time()
    
    if get_sizeof_list:
        return segment_dict, sizeof_list
    
    return segment_dict
    
def add_event_segment_dict(
    event_id, segment_dict=None, max_depth=None, max_num_tracks=None):
    """Create or augment a dictionary with tracks from an event."""
    if segment_dict is None:
        segment_dict = {CHILDREN: {}, WEIGHT: 0}
    if max_depth is None:
        max_depth = 20
    
    # iterate over tracks to perform updates
    for track in iter_tracks(event_id, max_num_tracks):
        # update flow_dict for each segment in track
        for i in range(len(track)):
            segment = track[i:i+max_depth]
            sd = segment_dict
            sd[WEIGHT] += 1
            for module_id in segment:
                if module_id not in sd[CHILDREN]:
                    sd[CHILDREN][module_id] = {CHILDREN: {}, WEIGHT: 0}
                
                sd = sd[CHILDREN][module_id]
                sd[WEIGHT] += 1


def iter_tracks(event_id, max_num_tracks=None):
    ordered_tracks = create_ordered_tracks_df(event_id)
    if max_num_tracks is None:
        max_num_tracks = len(ordered_tracks.index.levels[0])
    
    particle_ids = ordered_tracks.index.levels[0][:max_num_tracks]
    for pid in particle_ids:
        # create track as a list of (layer_id, volume_id, module_id) tuples
        # with terminating id strings "start" and "end" added to the beginning
        # and end.
        iter_rows = ordered_tracks.loc[pid].iterrows()
        module_list = list(tuple(row[1]) for row in iter_rows)
        yield ["start"] + module_list + ["end"]


def create_ordered_tracks_df(event_id):
    # Load data
    hits = pd.read_csv(file_url("hits", event_id))
    truth = pd.read_csv(file_url("truth", event_id))
    hit_orders = pd.read_csv(file_url("hit_orders", event_id))

    # merge to create hits_truth_orders
    hits_truth = pd.merge(hits, truth, on=['hit_id'])
    hits_truth_orders = pd.merge(
        hits_truth, hit_orders,
        on=['particle_id','hit_id']
    )
    
    # select cols, set index and sort to create ordered_tracks
    col_list = ["volume_id", "layer_id", "module_id", "particle_id", "hit_order"]
    ordered_tracks = hits_truth_orders.loc[:, col_list]
    
    ordered_tracks.set_index(["particle_id", "hit_order"], inplace=True)
    ordered_tracks.sort_index(inplace=True)
    
    return ordered_tracks

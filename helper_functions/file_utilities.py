"""Utilities for interacting with files.

These methods are specific to our team's SageMaker environment.
"""

__authors__ = ['Trenton Osborn']

def file_url(category, event_id=None, train_or_test="train"):
    """Returns the path of a csv corresponding to a given event and data
    category.
    
    Arguments:
    category -- one of "cells", "hits", "particles", "truth", "detectors",
        "sample_submission" or "hit_orders".
    event_id -- the integer id of an event. Should be included unless
        category is "detectors" or "sample submission". Ensure that event_id
        and train_or_test are consistent with each other.
    train_or_test -- one of "train" (default) or "test".
    """
    if category == 'hit_orders':
        folder = 'particles-in-order'
    elif category in ('sample_submission', 'detectors'):
        return '/home/ec2-user/SageMaker/efs/codalab_dataset/{0}.csv'.format(category)
    else:
        folder = 'codalab_dataset/' + train_or_test
    
    return '/home/ec2-user/SageMaker/efs/{0}/event{1:09d}-{2}.csv'.format(
        folder, event_id, category)

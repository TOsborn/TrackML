"""Find the order of hits in a ground truth track.

Methods are included to generate dataframes having columns ['particle_id', 'hit_id',
'hit_order'] and write the results to csv.
"""

__authors__ = ['Trenton Osborn']

import sys
import pandas as pd
import numpy as np

trackml_path = '/home/ec2-user/SageMaker/TrackML'
if trackml_path not in sys.path:
    sys.path.append(trackml_path)
    
from helper_functions.file_utilities import file_url


def write_hit_orders_csv(event_id):
    """Writes hit_order csv for an event."""
    generate_hit_orders(event_id).to_csv(file_url('hit_orders', event_id), index=False)

def generate_hit_orders(event_id):
    """Generates hit_order dataframe for an event.
    
    When finished, prints the number of valid particles and hits as well as the number and
    percentage of particles which were successfully placed in order.
    """
    # load truth, blacklist_particles and blacklist_hits files.
    truth = pd.read_csv(file_url('truth', event_id))

    particle_num_hits = truth.groupby('particle_id')['particle_id'].transform('count')
    not_short_track = particle_num_hits > 3
    del particle_num_hits
    
    not_particle_zero = truth.particle_id != 0
    
    truth = truth[not_particle_zero & not_short_track]
    del not_particle_zero, not_short_track
    
    particle_weight = truth.groupby('particle_id')['weight'].transform('sum')
    truth.loc[:, 'weight_order'] = truth.weight/particle_weight
    del particle_weight
    
    truth = truth[['particle_id', 'hit_id', 'tz', 'tpz', 'weight_order']]
    
    # create z_order_dim. This is tz if the z-dimension of the particle's average trajectory
    # is positive and -tz otherwise.
    z_direction = np.sign(truth.groupby('particle_id').tpz.transform('mean'))
    truth.loc[:, 'z_order_dim'] = z_direction*truth.tz
    truth.drop(['tz', 'tpz'], axis=1, inplace=True)
    del z_direction
    
    # create hit_order column.
    truth.loc[:, 'hit_order'] = truth.groupby('particle_id')['z_order_dim'].rank(
        method='first',
        ascending=True
    ).astype(int)
    truth.drop('z_order_dim', axis=1, inplace=True)

    # sort by particle_id and hit_order.
    truth.sort_values(['particle_id', 'hit_order'], inplace=True)
    
    truth.loc[:, 'track_length'] = truth.groupby('particle_id').hit_id.transform('count')
    true_weight_order = truth.groupby(['track_length', 'hit_order']).weight_order.median()
    truth.drop('track_length', axis=1, inplace=True)
    
    # identify and remove particles whose hit order is incorrect.
    # print('truth.groupby particle', truth.groupby('particle_id').values)
    particles_in_order = truth.groupby('particle_id').apply(_correct_order(true_weight_order))
    
    total_num_particles = len(particles_in_order)
    mask = particles_in_order.loc[truth.particle_id].values
    truth = truth[mask]
    num_good_particles = len(truth.particle_id.unique())
    
    truth.reset_index(drop=True, inplace=True)
    truth.drop('weight_order', axis=1, inplace=True)
    
    print('total number of scored particles in event:\t', total_num_particles)
    print('number of successfully sorted particles:\t', num_good_particles)
    print('percentage of partices successfully sorted\t:', 
          100*num_good_particles/total_num_particles)

    return truth

def _correct_order(true_weight_order):
    """Helper function for generate_hit_orders."""
    return lambda particle: np.all(
        np.isclose(
            particle.weight_order.values, true_weight_order.loc[len(particle)].values,
            atol=1e-06
        )
    ) 

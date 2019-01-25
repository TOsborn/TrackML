"""
Contains helper methods and constants for TrackSegment
"""

from track_segment import CHILDREN, WEIGHT

track_list = [
    [(1, 2, 3), (2, 3, 4)],
    [(1, 2, 3), (3, 4, 5)],
    [(2, 3, 4), (4, 5, 6), (5, 6, 7)],
    [(6, 7, 8)]
]


flow_dict = {
    # outermost layer contains all modules
    CHILDREN: {
        # children of "start" contain the first hit in a track.
        "start": {
            CHILDREN: {
                (1, 2, 3): {
                    CHILDREN: {
                        (2, 3, 4): {
                            CHILDREN: {
                                "end": {
                                    CHILDREN: {},
                                    WEIGHT: 1
                                }
                            },
                            WEIGHT: 1
                        },
                        (3, 4, 5): {
                            CHILDREN: {
                                # parents of "end" are the last hit in a track.
                                "end": {
                                    CHILDREN: {},
                                    WEIGHT: 1
                                }
                            },
                            WEIGHT: 1
                        }
                        
                    },
                    WEIGHT: 2
                },
                (2, 3, 4): {
                    CHILDREN: {
                        (4, 5, 6): {
                            CHILDREN: {
                                (5, 6, 7): {
                                    CHILDREN: {
                                        "end": {
                                            CHILDREN: {},
                                            WEIGHT: 1
                                        }
                                    },
                                    WEIGHT: 1
                                }
                            },
                            WEIGHT: 1
                        }
                    },
                    WEIGHT: 1
                },
                (6, 7, 8): {
                    CHILDREN: {
                        "end": {
                            CHILDREN: {},
                            WEIGHT: 1
                        }
                    },
                    WEIGHT: 1
                }
            },
            # weight of root is the number of particles in the entire dataset
            WEIGHT: 4,
        },
        (1, 2, 3): {
            CHILDREN: {
                (2, 3, 4): {
                    CHILDREN: {
                        "end": {
                            CHILDREN: {},
                            WEIGHT: 1
                        }
                    },
                    WEIGHT: 1
                },
                (3, 4, 5): {
                    CHILDREN: {
                        "end": {
                            CHILDREN: {},
                            WEIGHT: 1
                        }
                    },
                    WEIGHT: 1
                }
            },
            WEIGHT: 2
        },
        (2, 3, 4): {
            CHILDREN: {
                (4, 5, 6): {
                    CHILDREN: {
                        (5, 6, 7): {
                            CHILDREN: {
                                "end": {
                                    CHILDREN: {},
                                    WEIGHT: 1
                                }
                            },
                            WEIGHT: 1
                        }
                    },
                    WEIGHT: 1
                }
            },
            WEIGHT: 2
        },
        (3, 4, 5): {
            CHILDREN: {
                "end": {
                    CHILDREN: {},
                    WEIGHT: 1
                }
            },
            WEIGHT: 1
        },
        (4, 5, 6): {
            CHILDREN: {
                (5, 6, 7): {
                    CHILDREN: {
                        "end": {
                            CHILDREN: {},
                            WEIGHT: 1
                        }
                    },
                    WEIGHT: 1
                },
            },
            WEIGHT: 1
        },
        (5, 6, 7): {
            CHILDREN: {
                "end": {
                    CHILDREN: {},
                    WEIGHT: 1
                }
            },
            WEIGHT: 1
        },
        (6, 7, 8): {
            CHILDREN: {
                "end": {
                    CHILDREN: {},
                    WEIGHT: 1
                }
            },
            WEIGHT: 1
        }
    },
    WEIGHT: 12
}
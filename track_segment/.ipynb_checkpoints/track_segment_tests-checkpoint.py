from particleflow import ParticleFlow

track_list = [
    [(1, 2, 3), (2, 3, 4)],
    [(1, 2, 3), (3, 4, 5)],
    [(2, 3, 4), (4, 5, 6), (5, 6, 7)],
    [(6, 7, 8)]
]
flow_dict = {
    # outermost layer contains all modules
    CHILDREN: {
        # root module. Children of this module contain the first hit in a track.
        ROOT_MODULE: {
            # children of root are the location of the first hit in a track
            CHILDREN: {
                (1, 2, 3): {
                    CHILDREN: {
                        (2, 3, 4): {
                            CHILDREN: {
                                END_MODULE: {
                                    CHILDREN: {},
                                    WEIGHT: 1
                                }
                            },
                            WEIGHT: 1
                        },
                        (3, 4, 5): {
                            CHILDREN: {
                                END_MODULE: {
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
                                        END_MODULE: {
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
                        ROOT_MODULE: {
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
                        END_MODULE: {
                            CHILDREN: {},
                            WEIGHT: 1
                        }
                    },
                    WEIGHT: 1
                },
                (3, 4, 5): {
                    CHILDREN: {
                        END_MODULE: {
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
                                END_MODULE: {
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
                END_MODULE: {
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
                        END_MODULE: {
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
                END_MODULE: {
                    CHILDREN: {},
                    WEIGHT: 1
                }
            },
            WEIGHT: 1
        },
        (6, 7, 8): {
            CHILDREN: {
                END_MODULE: {
                    CHILDREN: {},
                    WEIGHT: 1
                }
            },
            WEIGHT: 1
        }
    },
    WEIGHT: 12
}

pf = ParticleFlow(flow_dict=flow_dict) 
root_module = pf.get_child(ROOT_MODULE)
print(pf.get_child((1, 2, 3)))

"""
UNIT TESTS 
"""

def test_iter_children():
    pass

def test_get_child():
    pf = ParticleFlow(flow_dict=flow_dict) 
    root_module = pf.get_child((1,2,3))

def test_get_descendant():
    pass

def test_get_parent():
    pass

def test_get_ancestor():
    pass

def test_get_root():
    pass

def test_get_segment():
    pass

def test_get_weight():
    pass

def test_init_child():
    pass
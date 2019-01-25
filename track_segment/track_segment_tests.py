from track_segment import TrackSegment, CHILDREN, WEIGHT
from track_segment_utils import track_list, flow_dict

"""
UNIT TESTS 
"""

def test_iter_children():
    ts = TrackSegment(flow_dict=flow_dict).get_child((1,2,3))
    children_expected = [ts.get_child(module_id) for module_id in [(2, 3, 4), (3, 4, 5)]]
    
    for child_result, child_expected in zip(ts.iter_children(), children_expected):
        assert(child_result is child_expected)
        
    print("TEST ITER_CHILDREN: success!")

def test_get_child():
    """
    Check that attributes of child are correct
    """
    
    root_ts = TrackSegment(flow_dict=flow_dict) 
    
    # ROOT MODULE
    start = root_ts.get_child("start")
    # check depth
    assert(start.depth == root_ts.depth+1)
    # check parent
    assert(start.parent is root_ts)
    # check module_id
    assert(start.module_id == 'start')
    
    # CHILD (1,2,3)
    root_ts_get_child_result = root_ts.get_child((1,2,3))
    # check depth
    assert(root_ts_get_child_result.depth == root_ts.depth+1)
    # check parent
    assert(root_ts_get_child_result.parent is root_ts)
    
    # CHILD (2,3,4)
    root_ts_get_child_result2 = root_ts_get_child_result.get_child((2,3,4))
    # check depth
    assert(root_ts_get_child_result2.depth == root_ts.depth+2)
    # check parent 
    assert(root_ts_get_child_result2.parent is root_ts_get_child_result)
    
    print("TEST GET_CHILD: success!")

    
def test_get_descendant():
    root_ts = TrackSegment(flow_dict=flow_dict)
    
    root_ts_descendant_result = root_ts.get_descendant([(1,2,3),(2,3,4)])
    
    root_ts_descendant_expected = root_ts.get_child((1,2,3)).get_child((2,3,4))    
    
    
    # Check if descendant is same as expected result
    assert(root_ts_descendant_result is root_ts_descendant_expected)
    
    # Check attributes of descendant 
    # depth
    assert(root_ts_descendant_result.depth == root_ts.depth+2)
    # parent
    assert(root_ts_descendant_result.parent is root_ts.get_child((1,2,3)))
    # module id 
    assert(root_ts_descendant_result.module_id == (2,3,4))
    
     # ROOT MODULE: check descendants starting from root module
    start = root_ts.get_child('start')
    
    start_descendant_result = start.get_descendant([(1,2,3),(2,3,4)])
    
    start_descendant_expected = start.get_child((1,2,3)).get_child((2,3,4))  
    
    # Check if descendant is same as expected result
    assert(start_descendant_result is start_descendant_expected)
    
     # Check attributes of descendant from root
    # depth
    assert(start_descendant_result.depth == start.depth+2)
    # parent
    assert(start_descendant_result.parent is start.get_child((1,2,3)))
    # module id 
    assert(start_descendant_result.module_id == (2,3,4))
    
    print("TEST GET_DESCENDANT: success!")
    

def test_get_parent():
    root_ts = TrackSegment(flow_dict=flow_dict) 

    # Call from root, result should be none
    start = root_ts.get_child('start')
    start_parent = start.get_parent()
    assert(start_parent.module_id is None)
    
    # Get parent of node one level down from parent
    child = root_ts.get_child((1,2,3))

    # validate get_parent
    parent = child.get_parent()
    assert(root_ts is parent)
    
    # check attributes
    # depth
    assert(parent.depth == 0)
    # module_id
    assert(parent.module_id is None)
    
    # Get parent which is not root
    child2 = child.get_child((2,3,4))
    
    # validate get_parent
    parent2 = child2.get_parent()
    assert(child is parent2)
    
    # check attributes
    # depth
    assert(parent2.depth == 1)
    # parent
    assert(parent2.parent is root_ts)
    # module_id
    assert(parent2.module_id == (1,2,3))

    print("TEST GET_PARENT: success!")
    

def test_get_ancestor():
    root_ts = TrackSegment(flow_dict=flow_dict)
    descendant = root_ts.get_descendant(['start', (1,2,3), (2,3,4)])
    
    # degree 1
    ancestor1 = descendant.get_ancestor(1)
    ancestor_expected1 = root_ts.get_descendant(['start', (1,2,3)])
    assert(ancestor1 is ancestor_expected1)
    
    # degree 2
    ancestor2 = descendant.get_ancestor(2)
    ancestor_expected2 = root_ts.get_descendant(['start'])
    assert(ancestor2 is ancestor_expected2)
    
    print("TEST GET_ANCESTOR: success!")
    

def test_get_first_module():
    root_ts = TrackSegment(flow_dict=flow_dict)
    
    root_first = root_ts.get_first_module()
    assert(root_first is None)
    
    ts1 = root_ts.get_child((1,2,3))
    ts1_first = ts1.get_first_module()
    assert(ts1_first is ts1)
    
    ts2 = root_ts.get_descendant([(1,2,3), (2,3,4)])
    ts2_first = ts2.get_first_module()
    assert(ts2_first is ts1)
    
    print("TEST GET_FIRST_MODULE: success!")
    

def test_get_ancestor_list():
    root_ts = TrackSegment(flow_dict=flow_dict)
    module_id_list = ['start', (1,2,3), (2,3,4), 'end']
    ts = root_ts.get_descendant(module_id_list)

    ancestor_list_result = ts.get_ancestor_list()
    ancestor_list_expected = [
        root_ts.get_descendant(module_id_list[:i+1])
        for i in range(4)
    ]
    
    for ancestor_result, ancestor_expected in zip(ancestor_list_result, ancestor_list_expected):
        assert(ancestor_result is ancestor_expected)
    
    print("TEST GET_ANCESTOR_LIST: success!")
    
def test_get_module_list():
    root_ts = TrackSegment(flow_dict=flow_dict)
    module_id_list = ['start', (1,2,3), (2,3,4), 'end']
    ts = root_ts.get_descendant(module_id_list)
    
    module_list_result = ts.get_module_list()
    
    for module_id_result, module_id_expected in zip(module_list_result, module_id_list):
        assert(module_id_result == module_id_expected)
        
    print("TEST GET_MODULE_LIST: success!")


test_iter_children()
test_get_child()
test_get_descendant()
test_get_parent()
test_get_ancestor()
test_get_first_module()
test_get_ancestor_list()
test_get_module_list()

# TODO: Account for cyclic tracks
# TODO: Add comments 

# global constants for indexing flow_dict
CHILDREN = 0
WEIGHT = 1

class TrackSegment:
    
    def __init__(self, threshold=1, max_depth=20, depth=0, parent=None, 
                   flow_dict=None, module_id=None, dict_fp=None):
        # set passed attributes
        self.threshold = threshold
        self.max_depth = max_depth
        self.depth = depth
        self.parent = parent
        self.module_id = module_id
        self.dict_fp = dict_fp
        
        # add logic to load flow dict
        # TODO
        
        # set weight
        self.weight = flow_dict[WEIGHT]
        
        # construct self.child_list and self.child_index_dict
        
        if depth < max_depth:
            # build self.child_list
            self.child_list = []
            for module_id in flow_dict[CHILDREN]:
                child_dict = flow_dict[CHILDREN][module_id]
                if child_dict[WEIGHT] >= threshold:
                    self.child_list.append(self._init_child(module_id, child_dict))
                
            self.child_list.sort(key=lambda ts: ts.get_weight(), reverse=True)
            
            # build dictionary of child indices
            self.child_index_dict = {
                child.module_id: index
                for index, child in enumerate(self.child_list)
            }
        else:
            self.child_list = []
            self.child_index_dict = {}
            
    
    def iter_children(self, threshold=None):
        # set threshold to self.threshold if it is None
        if threshold is None:
            threshold = self.threshold
            
        # iterate over children with weight above threshold
        i = 0
        while i < len(self.child_list) and self.child_list[i].weight >= threshold:
            yield self.child_list[i]
            i += 1
            
            
    def get_child(self, module_id):
        if module_id in self.child_index_dict:
            return self.child_list[self.child_index_dict[module_id]]
        else:
            return ParticleFlow(parent=self, flow_dict={CHILDREN: {}, WEIGHT: 0})
        
        
    def get_descendant(self, module_list):
        ts = self
        for module_id in module_list:
            ts = ts.get_child(module_id)
            
        return ts
    
    
    def get_module_id(self):
        return self.module_id
    
    
    def get_parent(self):
        return self.parent
    
    
    def get_ancestor(self, degree):
        if self.depth <= degree:
            return None
        
        if degree == 0:
            return self
        
        return self.get_parent().get_ancestor(degree-1)
    

    def get_first_module(self):
        if self.depth == 0:
            return None
        
        return self.get_ancestor(self.depth-1)

    
    def get_ancestor_list(self):
        def rec(ts, ancestor_list=[]):
            if ts and ts.get_module_id():
                ancestor_list.append(ts)
                rec(ts.get_parent(), ancestor_list)
                
            return ancestor_list
        
        ancestor_list = rec(self)
        ancestor_list.reverse()
        return ancestor_list
    
    
    def get_module_list(self):
        return [ancestor.get_module_id() for ancestor in self.get_ancestor_list()]
    
    
    def get_weight(self, module_list=[]):
        return self.get_descendant(module_list).weight
    
    
    def _init_child(self, module_id, child_dict):
        return TrackSegment(
            threshold=self.threshold,
            max_depth=self.max_depth,
            depth=self.depth+1,
            parent=self,
            flow_dict=child_dict,
            module_id=module_id
        )
    
    
    def __str__(self):
        newline_and_indent = "\n" + 37*" "
        
        ancestor_string = newline_and_indent.join([
            repr(ancestor.get_module_id()) + ", " + str(ancestor.get_weight())
            for ancestor in self.get_ancestor_list()
        ])
        
        children_string = newline_and_indent.join([
            repr(child.module_id) + ", " + str(child.get_weight())
            for child in self.child_list
        ])
        
        child_index_dict_string = "{" + newline_and_indent.join([
            repr(key) + ": " + str(val)
            for key, val in self.child_index_dict.items()
        ]) + "}"
            
        return (
            """
__________________________________________
ParticleFlow Instance:

    threshold:                       {0}
    max_depth:                       {1}
    depth:                           {2}
    dict_fp:                         {3}

    module sequence (id, weight):    {4}

    children (id, weight):           {5}

__________________________________________
            """
        ).format(
            self.threshold,            # 0
            self.max_depth,            # 1
            self.depth,                # 2
            self.dict_fp,              # 3
            ancestor_string,           # 4
            children_string,           # 5
        )
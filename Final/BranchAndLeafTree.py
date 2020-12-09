from random import sample, random
from ast import literal_eval
from neighbor_joining import calculate_distance_to_new_node
from copy import deepcopy

class BranchAndLeafTree:
    parents = dict()#child to parent
    internal_nodes = dict()#name to depth)
    leaves = dict()#name to depth
    last_internal_node = -1
    dist_dict = dict()
    current_length = int()
    
    #Creates a BranchAndLeafTree object from a cladogram
    def __init__(self, cladogram, dist_dict):
        self.dist_dict = deepcopy(dist_dict)
        self.internal_nodes["_0"] = 0
        self.last_internal_node = 0
        self.find_branches(cladogram[0], cladogram[2], "_0", 1)
        self.current_length = self.calculate_length()
            
    #Recursive function for initializing a BranchAndLeafTree object
    #@Param clade1: One of two clades being passed to this function
    #@Param clade2: One of two clades being passed to this function
    #@Param parent: The string being used to represent the parent node of these clades
    #Return: nothing
    def find_branches(self, clade1, clade2, parent, depth):
        if(type(clade1) == tuple):
            self.last_internal_node += 1
            self.internal_nodes["_" + str(self.last_internal_node)] = depth
            self.parents["_" + str(self.last_internal_node)] = parent
            self.find_branches(clade1[0], clade1[2], "_" + str(self.last_internal_node), depth + 1)
        else:
            self.leaves[str(clade1)] = depth
            self.parents[str(clade1)] = parent
        if(type(clade2) == tuple):
            self.last_internal_node += 1
            self.internal_nodes["_" + str(self.last_internal_node)] = depth 
            self.parents["_" + str(self.last_internal_node)] = parent
            self.find_branches(clade2[0], clade2[2], "_" + str(self.last_internal_node), depth + 1)
        else:
            self.leaves[str(clade2)] = depth
            self.parents[str(clade2)] = parent
        return          
    
    #Returns a cladogram representation of this object
    #Return: A cladogram of the graph
    def to_cladogram(self):
        #0,2 names, 1, 3 distances
        self.fix_subtree('_0')
        leaves_copy = deepcopy(self.leaves)
        parents_copy = deepcopy(self.parents)
        max_depth = 0
        for leaf in leaves_copy:
            if leaves_copy[leaf] > max_depth:
                max_depth = leaves_copy[leaf]
        leaves_at_max_depth = set()
        while len(leaves_copy) > 1:
            #Find leaves at current depth
            for leaf in leaves_copy:
                if leaves_copy[leaf] == max_depth:
                    leaves_at_max_depth.add(leaf)
            for leaf in leaves_at_max_depth:
                leaves_copy.pop(leaf)
            max_depth -= 1
            while len(leaves_at_max_depth) > 0:
                first = leaves_at_max_depth.pop()
                if first[0] == '(':
                    first = literal_eval(first)
                parent = parents_copy[str(first)]
                second = ""
                parents_copy.pop(str(first))
                for key in parents_copy:
                    if parents_copy[key] == parent:
                        second = key
                        if second[0] == '(':
                            second = literal_eval(second)
                        parents_copy.pop(key)
                        break
                leaves_copy[str((first, second))] = max_depth
                if parent != '_0':
                    parents_copy[str((first, second))] = parents_copy[parent]
                    parents_copy.pop(parent)
                leaves_at_max_depth.remove(str(second))
        for leaf in leaves_copy:
            return leaf
    
    #Branch swapping algorithm to look for a better tree
    #@Param iterations: The number of swaps to be attampted
    #@Param accept_rate: The rate at which worse swaps should be accepted
    #Return: nothing
    def branch_swapping(self, iterations = 1000, accept_rate = 0.3):
        best_leaves = deepcopy(self.leaves)
        best_parents = deepcopy(self.parents)
        best_internal_nodes = deepcopy(self.internal_nodes)
        best_length = self.current_length
        #The initial tree length
        for _ in range(iterations):
            current_internal_nodes = deepcopy(self.internal_nodes)
            current_parents = deepcopy(self.parents)
            current_leaves = deepcopy(self.leaves)
            #randomly picks a leaf to move
            leaf = sample(list(self.leaves), 1)[0]
            #Randomly picks a branch to add the leaf to
            splice_site = sample(list(self.parents), 1)[0]
            #TODO: Add the leaf
            self.last_internal_node += 1
            self.internal_nodes["_" + str(self.last_internal_node)] = self.internal_nodes[self.parents[splice_site]] + 1
            self.parents["_" + str(self.last_internal_node)] = self.parents[splice_site]
            self.leaves[leaf] = self.internal_nodes[self.parents[splice_site]] + 2
            self.parents[leaf] = "_" + str(self.last_internal_node)
            self.parents[splice_site] = "_" + str(self.last_internal_node)
            if splice_site in self.leaves:
                self.leaves[splice_site] = self.leaves[leaf]
            else:
                self.internal_nodes[splice_site] = self.leaves[leaf]
            self.fix_subtree("_0")
            #TODO: Calculate new length
            new_length = self.calculate_length()
            if new_length < best_length:
                best_leaves = deepcopy(self.leaves)
                best_parents = deepcopy(self.parents)
                best_internal_nodes = deepcopy(self.internal_nodes)
            elif random() >= accept_rate:#choose not to take a step backwards
                self.leaves = deepcopy(current_leaves)
                self.parents = deepcopy(current_parents)
                self.internal_nodes = deepcopy(current_internal_nodes)
        self.parents = deepcopy(best_parents)
        self.leaves = deepcopy(best_leaves)
        self.internal_nodes = deepcopy(best_internal_nodes)
        return

    #Find the set notation for the subtree of a specified node
    #@Param node_name: The name of the node to find the subtree of
    #Return: The set notation of the subtree
    def fix_subtree(self, node_name):
        if node_name == "_0":
            internal_node_counter = dict()
            to_remove = list()
            for child in self.parents:
                if not child in self.leaves and not child in self.internal_nodes:
                    to_remove.append(child)
            for trash in to_remove:
                self.parents.pop(trash)
            for node in self.internal_nodes:
                internal_node_counter[node] = list();
            for child in self.parents:
                internal_node_counter[self.parents[child]].append(child)
            is_changed = True
            while is_changed:
                is_changed = False
                for node in internal_node_counter:
                    if node == node_name:
                        continue
                    if len(internal_node_counter[node]) == 0:
                        if node == '_0':
                            continue
                        if node in self.internal_nodes:
                            self.internal_nodes.pop(node)
                            internal_node_counter[self.parents[node]].remove(node)
                            self.parents.pop(node)
                            is_changed = True
                    elif len(internal_node_counter[node]) == 1:
                        if node == '_0':
                            continue
                        self.parents[internal_node_counter[node][0]] = self.parents[node]
                        if internal_node_counter[node][0] in self.internal_nodes:
                            self.internal_nodes[internal_node_counter[node][0]] = self.internal_nodes[node]
                        elif internal_node_counter[node][0] in self.leaves:
                            self.leaves[internal_node_counter[node][0]] = self.internal_nodes[node]
                        self.internal_nodes.pop(node)
                        internal_node_counter[self.parents[node]].remove(node)
                        internal_node_counter[self.parents[node]].append(internal_node_counter[node][0])
                        internal_node_counter[node].pop(0)
                        self.parents.pop(node)
                        is_changed = True
                    
            to_update = list()
            to_update.append('_0')
            while len(to_update) > 0:
                node = to_update[0]
                to_update.pop(0)
                if node in internal_node_counter:
                    for child in internal_node_counter[node]:
                        to_update.append(child)
                if node == '_0':
                    continue
                elif node in self.internal_nodes:
                    self.internal_nodes[node] = self.internal_nodes[self.parents[node]] + 1
                elif node in self.leaves:
                    self.leaves[node] = self.internal_nodes[self.parents[node]] + 1
            
    #Calculates the length of the tree in its current state
    #@Return: The length of the tree
    def calculate_length(self):
        leaves_copy = deepcopy(self.leaves)
        parents_copy = deepcopy(self.parents)
        dist_copy = deepcopy(self.dist_dict)
        length = 0
        max_depth = 0
        for leaf in leaves_copy:
            if leaves_copy[leaf] > max_depth:
                max_depth = leaves_copy[leaf]
        leaves_at_max_depth = set()
        while len(leaves_copy) > 1:
            #Find leaves at current depth
            for leaf in leaves_copy:
                if leaves_copy[leaf] == max_depth:
                    leaves_at_max_depth.add(leaf)
    
            #removes leaves at max depth from list of leaves
            for leaf in leaves_at_max_depth:
                leaves_copy.pop(leaf)
            
            #sets new max depth for next iteration
            max_depth -= 1
            #pairs off all of the leaves that were at the maximum depth
            while len(leaves_at_max_depth) > 0:
                first = leaves_at_max_depth.pop()
                #if the first element is an internal node, convert it to a tuple
                if first[0] == '(':
                    first = literal_eval(first)
                
                #find the parent node to replace
                parent = parents_copy[str(first)]
                #placeholder for the second half of the tuple
                second = ""
                #remove the first half from the parents array so it cannot be found
                parents_copy.pop(str(first))
                if len(leaves_at_max_depth) == 0:
                    leaves_copy[str(first)] = max_depth
                    parents_copy[str(first)] = parents_copy[parent]
                    continue
                #Iterate through all leaves at max depth and find the one that pairs with first
                for key in leaves_at_max_depth:
                    if parents_copy[key] == parent:
                        second = key
                        #convert string to tuple as necessary
                        if second[0] == '(':
                            second = literal_eval(second)
                        #remove second and final reference to parent from parents
                        parents_copy.pop(key)
                        break
                if second == "":
                    leaves_copy[str(first)] = max_depth
                    parents_copy[str(first)] = parents_copy[parent]
                    continue
                #sets depth of new leaf to new max depth
                leaves_copy[str((first, second))] = max_depth
                #creates the tuple
                new_node = (first, second)
                #Finds distances to the new node from each child
                dfirst, dsecond = calculate_distance_to_new_node(dist_copy, str(first), str(second))
                dist_copy[str(new_node)] = dict()
                #inserts these values into the distance dict
                dist_copy[str(first)][str(new_node)] = dfirst
                dist_copy[str(new_node)][str(first)] = dfirst
                dist_copy[str(second)][str(new_node)] = dsecond
                dist_copy[str(new_node)][str(second)] = dsecond
                #increase the length by these two edges
                length += dfirst + dsecond
                #populate dist dict
                for key in list(dist_copy.keys()):
                    if first == key or second == key:
                        continue
                    d = (dist_copy[str(first)][str(key)] + dist_copy[str(second)][str(key)] - dist_copy[str(first)][str(second)]) / 2
                    dist_copy[str(new_node)][str(key)] = d
                    dist_copy[str(key)][str(new_node)] = d
                #if parent != '_0':
                if parent in parents_copy:
                    parents_copy[str((first, second))] = parents_copy[parent]
                    parents_copy.pop(parent)
                elif parent in self.parents:
                    parents_copy[str((first, second))] = self.parents[parent]
        
                leaves_at_max_depth.remove(str(second))
        return length
            
                

def test():
#This function tests the above Class
    from distance import dJC
    import upgma

    t = {
        'A': "ATATAT",
        'B': "ATTTTT",
        'C': "ATATAA",
        'D': "TTTTTT"
    }
    
    some = upgma.make_dist_dict(t, dJC)

    print(some)

    res = upgma.make_cladogram(some.copy())

    print(res)

    tree = BranchAndLeafTree(res, some)

    tree.branch_swapping()

    clad = tree.to_cladogram()
    print(clad)

    import output_tree
    output_tree.output_tree(clad, "test", "mytree.png")

if __name__ == '__main__':
    test()
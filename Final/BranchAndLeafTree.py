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
        self.current_length = self.calculate_length()
        self.internal_nodes["_0"] = 0
        self.last_internal_node = 0
        self.find_branches(cladogram[0], cladogram[2], "_0", 1)
            
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
        children = list()
        for child in self.parents:
            if self.parents[child] == node_name:
                children.append(child)
        if len(children) == 2:
            self.parents[children[0]] = node_name
            self.parents[children[1]] = node_name
            for child in children:
                if child[0] == "_":
                    self.internal_nodes[child] = self.internal_nodes[node_name] + 1
                else:
                    self.leaves[child] = self.internal_nodes[node_name] + 1
            if children[0][0] == "_":
                self.fix_subtree(children[0])
            if children[1][0] == "_":
                self.fix_subtree(children[1])
        elif len(children) == 1 and node_name != "_0":
            for node in self.internal_nodes:
                if self.parents[node_name] == node:
                    self.parents[children[0]] = node
                    if children[0][0] == '_':
                        self.internal_nodes[children[0]] = self.internal_nodes[node] + 1
                        self.fix_subtree(children[0])
                    else:
                        self.leaves[children[0]] = self.internal_nodes[node] + 1
                    break
            self.internal_nodes.pop(node_name)
            self.parents.pop(node_name)
        elif node_name != "_0":
            if node_name[0] == "_":
                self.internal_nodes.pop(node_name)
                self.parents.pop(node_name)
        else:
            self.fix_subtree(children[0])
            
    def calculate_length(self):
        #names = dict()#internal node to string representation
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
            print(leaves_at_max_depth)
            print(parents_copy)
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
                if len(leaves_at_max_depth) == 0:
                    leaves_copy[str(first)] = max_depth
                    continue
                for key in leaves_at_max_depth:
                    if parents_copy[key] == parent:
                        second = key
                        if second[0] == '(':
                            second = literal_eval(second)
                        parents_copy.pop(key)
                        break
                leaves_copy[str((first, second))] = max_depth
                new_node = (first, second)
                #print(self.to_cladogram())
                #print(self.parents)
                print()
                dfirst, dsecond = calculate_distance_to_new_node(dist_copy, str(first), str(second))
                dist_copy[str(new_node)] = dict()
                dist_copy[str(first)][str(new_node)] = dfirst
                dist_copy[str(new_node)][str(first)] = dfirst
                dist_copy[str(second)][str(new_node)] = dsecond
                dist_copy[str(new_node)][str(second)] = dsecond
                length += dfirst + dsecond
                for key in list(dist_copy.keys()):
                    if first == key or second == key:
                        continue
                    d = (dist_copy[str(first)][str(key)] + dist_copy[str(second)][str(key)] - dist_copy[str(first)][str(second)]) / 2
                    dist_copy[str(new_node)][str(key)] = d
                    dist_copy[str(key)][str(new_node)] = d
                if parent != '_0':
                    print(str((first, second)))
                    parents_copy[str((first, second))] = parents_copy[parent]
                    parents_copy.pop(parent)
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
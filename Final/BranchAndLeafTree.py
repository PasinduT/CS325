from random import sample, random
from ast import literal_eval

class BranchAndLeafTree:
    parents = dict()#child to parent
    internal_nodes = dict()#name to depth)
    leaves = dict()#name to depth
    last_internal_node = -1
    
    #Creates a BranchAndLeafTree object from a cladogram
    def __init__(self, cladogram):
        self.internal_nodes["_0"] = 0
        self.last_internal_node = 0
        self.find_branches(cladogram[0], cladogram[1], "_0", 1)
            
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
            self.find_branches(clade1[0], clade1[1], "_" + str(self.last_internal_node), depth + 1)
        else:
            self.leaves[str(clade1)] = depth
            self.parents[str(clade1)] = parent
        if(type(clade2) == tuple):
            self.last_internal_node += 1
            self.internal_nodes["_" + str(self.last_internal_node)] = depth 
            self.parents["_" + str(self.last_internal_node)] = parent
            self.find_branches(clade2[0], clade2[1], "_" + str(self.last_internal_node), depth + 1)
        else:
            self.leaves[str(clade2)] = depth
            self.parents[str(clade2)] = parent
        return          
    
    #Returns a cladogram representation of this object
    #Return: A cladogram of the graph
    def to_cladogram(self):
        leaves_copy = self.leaves.copy()
        parents_copy = self.parents.copy()
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
            print("Leaves")
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
        best_leaves = self.leaves.copy()
        best_parents = self.parents.copy()
        best_internal_nodes = self.internal_nodes.copy()
        #best_length = 
        #The branch that was removed
        #best_length = 
        for _ in range(iterations):
            print("Start")
            current_internal_nodes = self.internal_nodes.copy()
            current_parents = self.parents.copy()
            current_leaves = self.leaves.copy()
            #randomly picks a leaf to move
            leaf = sample(list(self.leaves), 1)[0]
            print("Leaf")
            print(leaf)
            #Randomly picks a branch to add the leaf to
            splice_site = sample(list(self.parents), 1)[0]
            print("Splice Site")
            print(splice_site)
            #TODO: Add the leaf
            self.last_internal_node += 1
            self.internal_nodes["_" + str(self.last_internal_node)] = self.internal_nodes[self.parents[splice_site]] + 1
            self.parents["_" + str(self.last_internal_node)] = self.parents[splice_site]
            self.leaves[leaf] = self.internal_nodes[self.parents[splice_site]] + 2
            self.parents[leaf] = "_" + str(self.last_internal_node)
            self.parents[splice_site] = "_" + str(self.last_internal_node)
            self.fix_subtree("_0")
            print(self.to_cladogram())
            #TODO: Calculate new length
            if new_length > best_length:
                best_leaves = self.leaves.copy()
                best_parents = self.parents.copy()
                best_internal_nodes = self.internal_nodes.copy()
            elif random() >= accept_rate:#choose not to take a step backwards
                self.leaves = current_leaves.copy()
                self.parents = current_parents.copy()
                self.internal_nodes = current_internal_nodes.copy()
        self.parents = best_parents.copy()
        self.leaves = best_leaves.copy()
        self.internal_nodes = best_internal_nodes.copy()
        return

    #Find the set notation for the subtree of a specified node
    #@Param node_name: The name of the node to find the subtree of
    #Return: The set notation of the subtree
    def fix_subtree(self, node_name):
        print(self.parents)
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

    res = upgma.make_cladogram(some)

    print(res)

    tree = BranchAndLeafTree(res)

    tree.branch_swapping()

    clad = tree.to_cladogram()
    print(clad)

    import output_tree
    output_tree.output_tree(clad, "test", "mytree.png")

if __name__ == '__main__':
    test()
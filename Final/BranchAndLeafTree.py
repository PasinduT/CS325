from random import sample
from ast import literal_eval

class BranchAndLeafTree:
    branches = set()
    parents = dict()#child to parent
    internal_nodes = dict()#string notation to (name, depth)
    leaves = dict()#name to depth
    
    #Creates a BranchAndLeafTree object from a cladogram
    def __init__(self, cladogram):
        self.internal_nodes[str(cladogram)] = ("_0", 0)
        self.find_branches(cladogram[0], cladogram[1], "_0", 1)
            
    #Recursive function for initializing a BranchAndLeafTree object
    #@Param clade1: One of two clades being passed to this function
    #@Param clade2: One of two clades being passed to this function
    #@Param parent: The string being used to represent the parent node of these clades
    #Return: nothing
    def find_branches(self, clade1, clade2, parent, depth):
        if(type(clade1) == tuple):
            self.internal_nodes[str(clade1)] = ("_" + str(len(self.internal_nodes)), depth)
            self.parents[str(self.internal_nodes[str(clade1)][0])] = parent
            self.branches.add((parent, self.internal_nodes[str(clade1)]))
            self.find_branches(clade1[0], clade1[1], self.internal_nodes[str(clade1)], depth + 1)
        else:
            self.leaves[str(clade1)] = depth
            self.parents[str(clade1)] = parent[0]
        if(type(clade2) == tuple):
            self.internal_nodes[str(clade2)] = ("_" + str(len(self.internal_nodes)), depth) 
            self.parents[str(self.internal_nodes[str(clade2)][0])] = parent
            self.branches.add((str(parent), str(self.internal_nodes[str(clade2)])))
            self.find_branches(clade2[0], clade2[1], self.internal_nodes[str(clade2)], depth + 1)
        else:
            self.leaves[str(clade2)] = depth
            self.parents[str(clade2)] = parent[0]
        return          
    
    #Returns a cladogram representation of this object
    #Return: A cladogram of the graph
    def to_cladogram(self):
        leaves_copy = self.leaves.copy()
        branch_copy = self.branches.copy()
        parents_copy = self.parents.copy()
        clad_parts = list()#(cladogram part, parent)
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
                second = 0
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
        best_branches = self.branches.copy()
        for _ in range(iterations):
            #randomly picks a leaf to move
            leaf = sample(list(self.leaves), 1)[0]
            #Removes the branch that the leaf was on
            for branch in self.branches:
                if(branch[1] == leaf):
                    self.branches.remove(branch)
                    break
            #Randomly picks a branch to add the leaf to
            splice_site = sample(self.branches, 1)[0]
            #TODO: Add the leaf, clean tree up, calculate new length
            #Cleaning tree up consists of removing unnecessary branches and
            #changing parents and depths. Probably a dfs problem?
        self.branches = best_branches
        return

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
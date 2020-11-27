from ete3 import Tree

def output_tree (the_tree, filename):
    t = Tree(str(the_tree) + ";")
    t.render(filename, w=183, units="mm")
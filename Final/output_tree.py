from ete3 import Tree, TreeStyle, TextFace, NodeStyle, add_face_to_node

def output_tree (the_tree, name, filename):
    t = Tree(tree_to_newick(the_tree) + ";")

    style = TreeStyle()
    style.title.add_face(TextFace(name, fsize=10), column=0)
    style.show_scale = True
    style.show_leaf_name = False


    birds = ['Red junglefowl', 'Downy Woodpecker', 'Barn owl',
    'Ruff', 'Zebra finch', 'White-throated Tinamou', 'Budgerigar',
    'Adélie penguin', 'Golden eagle', 'Gyrfalcon', 
    'Common ostrich', 'Mallard', 'A']
    squamates = ['Sand lizard','Tiger snake','Eastern brown snake','Carolina anole',]
    crocadillians = ['American alligator', 'Gharial','C']
    turtles = ['Green sea turtle', 'Painted turtle','D']

    t.unroot()

    for n in t.traverse():
        nstyle = NodeStyle()
        n.add_face(TextFace(' ' + n.name, fsize=2), 1)

        if n.is_leaf():
            leafname = str(n.name)
            if leafname in birds:
                nstyle["fgcolor"] = "aqua"
            elif leafname in squamates:
                nstyle["fgcolor"] = "yellow"
            elif leafname in crocadillians:
                nstyle["fgcolor"] = "lightgreen"
            elif leafname in turtles:
                nstyle["fgcolor"] = "orange"
        else:
            nstyle['fgcolor'] = 'black'
            nstyle['size'] = 0

        n.set_style(nstyle)

    t.render(filename, tree_style=style, w=1024, units="mm")

def tree_to_newick (tree):
    if type(tree) == str:
        return tree
    
    # Otherwise the tree better be a tuple
    if len(tree) == 3:
        a, d, b = tree
        return '({}, {})'.format(tree_to_newick(a), tree_to_newick(b))

    elif len(tree) == 4:
        a, da, b, db = tree
        return '({}:{}, {}:{})'.format(tree_to_newick(a), da, tree_to_newick(b), db)

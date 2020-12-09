from ete3 import Tree, TreeStyle, TextFace, NodeStyle, add_face_to_node
import re

# This function uses the ETE library to generate an image of the phylogenetic
# tree that is passed on to it
# the_tree: the tree that should displayed in FORMAT_1
# name: the name of the tree that will be added to the top of the image
# filename: the filename to which the resultant image will be written to
def output_tree (the_tree, name, filename):

    # Create a new tree object and by converting the tree in FORMAT_1 to 
    # the newick format accepted by ETE
    t = Tree(tree_to_newick(the_tree) + ";")

    # Unroot the tree (by default ETE recognizes all trees are rooted)
    t.unroot()

    # Make a new style object that would have features to stylize the ETE tree
    style = TreeStyle()
    style.title.add_face(TextFace(name, fsize=5), column=0)
    style.show_scale = False
    style.show_leaf_name = False

    # Since birds, squamates, crocodillians, and turtles have their own color
    # scheme, separate them into lists
    birds = ['Red junglefowl', 'Downy Woodpecker', 'Barn owl',
        'Ruff', 'Zebra finch', 'White-throated Tinamou', 'Budgerigar',
        'Adélie penguin', 'Golden eagle', 'Gyrfalcon', 
        'Common ostrich', 'Mallard', 'A']
    squamates = ['Sand lizard','Tiger snake','Eastern brown snake',
        'Carolina anole',]
    crocodilians = ['American alligator', 'Gharial','C']
    turtles = ['Green sea turtle', 'Painted turtle','D']

    # Use regex to parse out the leafname (sometimes it has quotes)
    regex = re.compile(r"[^']+" )

    
    # Loop through all the nodes in the tree
    for n in t.traverse():
        # Make a new node style object and add the leaf name to it
        nstyle = NodeStyle()

        # If the node is a leaf the add the correct color scheme to it, and 
        # make sure that the leaf name is visible
        if n.is_leaf():
            # Get the proper leaf name
            leafname = regex.search(n.name).group(0)
            n.add_face(TextFace(' ' + leafname, fsize=2), 1)

            if leafname in birds:
                nstyle["fgcolor"] = "aqua"
            elif leafname in squamates:
                nstyle["fgcolor"] = "yellow"
            elif leafname in crocodilians:
                nstyle["fgcolor"] = "lightgreen"
            elif leafname in turtles:
                nstyle["fgcolor"] = "orange"
        else:
            # Otherwise don't display the node
            nstyle['fgcolor'] = 'black'
            nstyle['size'] = 0

        # Finally attach the node style object to the node
        n.set_style(nstyle)

    # Attach the tree style object to the tree, and then render the tree on
    # an image name `filename` that is 1024mm wide. The height will adjust 
    # automatically.
    t.render(filename, tree_style=style, w=1024, units="mm")

# This will convert a tree given in FORMAT_1 to a newick string representation
# of the tree that is accepted by the ETE tree library
# tree: the tree in FORMAT_1
# Return: a newick string representation of the tree that was passed on
def tree_to_newick (tree):
    # If it is a string, then return a string
    if type(tree) == str:
        return tree
    
    # Otherwise the tree better be a tuple
    # If the tuple has three elements (the topmost node) print it as an empty 
    # tuple without distances
    if len(tree) == 3:
        a, d, b = tree
        return '({}, {})'.format(tree_to_newick(a), tree_to_newick(b))
    # Otherwise (any other node) print it with the distances.
    elif len(tree) == 4:
        a, da, b, db = tree
        return '({}, {})'.format(tree_to_newick(a), 
            tree_to_newick(b))

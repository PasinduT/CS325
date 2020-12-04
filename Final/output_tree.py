from ete3 import Tree, TreeStyle, TextFace, NodeStyle

def output_tree (the_tree, name, filename):
    t = Tree(str(the_tree) + ";")

    style = TreeStyle()
    style.title.add_face(TextFace(name, fsize=10), column=0)
    style.show_scale = False
    style.scale = 80


    birds = ["'Red junglefowl'", "'Downy Woodpecker'", "'Barn owl'",
    "'Ruff'", "'Zebra finch'", "'White-throated Tinamou'", "'Budgerigar'",
    "'Adélie penguin'", "'Golden eagle'", "'Gyrfalcon'", 
    "'Common ostrich'", "'Mallard'", "'A'"]
    squamates = ["'Sand lizard'","'Tiger snake'","'Eastern brown snake'","'Carolina anole'",]
    crocadillians = ["'American alligator'", "'Gharial'","'C'"]
    turtles = ["'Green sea turtle'", "'Painted turtle'","'D'"]

    for n in t.traverse():
        nstyle = NodeStyle()
        nstyle['size'] = 10
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
            if n.is_root():
                nstyle['size'] = 10

        n.set_style(nstyle)

    t.render(filename, tree_style=style, w=220, units="mm")
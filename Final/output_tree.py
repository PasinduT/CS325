from ete3 import Tree, TreeStyle, TextFace, NodeStyle

def output_tree (the_tree, name, filename):
    t = Tree(str(the_tree) + ";")

    style = TreeStyle()
    style.title.add_face(TextFace(name, fsize=10), column=0)
    style.show_scale = False
    style.scale = 80

    nstyle = NodeStyle()
    nstyle['size'] = 10

    for n in t.traverse():
        n.set_style(nstyle)

    t.render(filename, tree_style=style, w=220, units="mm")
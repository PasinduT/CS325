import os
from upgma import make_dist_dict
from neighbor_joining import make_cladogram
from fasta import readFASTAFile
from distance import dJC
from dp_distance import dp_distance as dp_dist
import output_tree
import json, re

# This function parses a filename of a fasta file containing a sequence
# for example if the filename is 'TPM1_A_gallus.fa', then it will return
# gallus.
# filename: the filename that should be parsed
# Return: returns the given output
filename_re = re.compile(r'\w+_([\w_]+)\.fa')
def parse_filename(filename):
    return filename_re.match(filename).group(1)


# FORMAT_1: the format in which the output tree from Neighbor Joining
#           will be stored
# The tree will be represented in a recursive format, where each node will be
# stored as a tuple. There are two types of nodes. The topmost node of the tree
# has the following format:
#           (Node A, distance between Node A and Node B, Node B)
# the reason for this is that Neighbor joining returns an unrooted tree, which 
# means that one of the branches must be given individually in a node based 
# format. 
# The second type of node is the internal node. For example internal node Node U
# has the following structure:
#   (Child Node A, distance to Node A, Child Node B, distance to Node B)
# All distances will be in Python floats, and leaf nodes will be stored as 
# strings.

# FORMAT_2: the format in which the distance matrix will be stored
#

# This is the main function of the program
def main():
    conversions = {
        "scutatus": "Tiger snake",
        "carolinensis": "Carolina anole",
        "picta": "Painted turtle",
        "mississippiensis": "American alligator",
        "platyrhynchos": "Mallard",
        "guttatus": "White-throated Tinamou",
        "chrysaetos": "Golden eagle",
        "mydas": "Green sea turtle",
        "guttata": "Zebra finch",
        "gallus": "Red junglefowl",
        "pugnax": "Ruff",
        "rusticolus": "Gyrfalcon",
        "undulatus": "Budgerigar",
        "agilis": "Sand lizard",
        "adeliae": "Adélie penguin",
        "camelus": "Common ostrich",
        "alba": "Barn owl",
        "gangeticus": "Gharial",
        "textilis": "Eastern brown snake",
        "pubescens": "Downy Woodpecker"
    }

    distances_dest = "output/distances/"
    sequences_src = "sequences/"

    for folder in os.listdir(sequences_src):
        genes = {}
        for filename in os.listdir(sequences_src + folder):
            name = conversions.get(parse_filename(filename), 
                parse_filename(filename))
            readFASTAFile(sequences_src + folder + "/" + filename, 
                name, genes)

        print(folder)
        print(list(genes.keys()))
        print([len(genes[a]) for a in genes])

        try:
            file = open(distances_dest + folder + '.json')
            some = json.load(file)
        except:
            print('Calculating distances...')
            some = make_dist_dict(genes, dp_dist, distances_dest + folder + '.json')

        # print(some.keys())

        res = make_cladogram(some)

        with open("output/tree_" + folder + '.txt' , 'w') as file:
            file.write('{}'.format(res))

        output_tree.output_tree(res, folder, 'output/' + folder + '.png')


if __name__ == '__main__':
    main()
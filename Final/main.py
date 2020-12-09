import os
from upgma import make_dist_dict
from neighbor_joining import make_cladogram
from fasta import readFASTAFile
from dp_distance import dp_distance as dp_dist
import output_tree
import json, re
from BranchAndLeafTree import BranchAndLeafTree
import copy

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
# Since most parts of the program requires a distance matrix between each 
# pair of sequences. We had to implement a version of a distance matrix. 
# Using a 2 dimensional array would require us to enumerate the sequences in a 
# way, preventing us from caching the results from a previous run at computing 
# the distances. Therefore we decided to use a structure consisting of nested
# dictionaries, where the both names and distances would be stored. For example,
# if we have the following distance matrix:
#        ___|_A_|_B_|_C__
#        A  | 0 | 1 | 3
#        B  | 1 | 0 | 2
#        B  | 3 | 2 | 0
# We would store it as:
# {
#   'A': {'B': 1, 'C': 3},
#   'B': {'A': 1, 'C': 2},
#   'C': {'A': 3, 'B': 2},
# }

# This is the main function of the program
def main():

    # Dictionary which converts the filenames to the common names of the species
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

    # The location of the cached files from the distance matrix function
    # since this is the most computationally intensive part of the program, 
    # storing it helps.
    distances_dest = "output/distances/"

    # The directory which contains the sequences, ordered into folders by the
    # type of gene it contains
    sequences_src = "sequences/"

    # Loop through every folder in the sequences directory
    for folder in os.listdir(sequences_src):

        # Obtain a list of all the genes from all the files
        genes = {}
        for filename in os.listdir(sequences_src + folder):
            name = conversions.get(parse_filename(filename), 
                parse_filename(filename))
            readFASTAFile(sequences_src + folder + "/" + filename, 
                name, genes)


        # Output here for debugging reasons
        print(folder)
        print(list(genes.keys()))
        print([len(genes[a]) for a in genes])

        # If there already exists .json files containing the distance matricies
        # in the distances_dest folder, then load the distances from that
        # instead of computing the distances again
        try:
            file = open(distances_dest + folder + '.json')
            some = json.load(file)
        except:
            # Otherwise calculate the distances 
            print('Calculating distances...')
            some = make_dist_dict(genes, dp_dist, distances_dest + folder + '.json')

        # Run the neighbor joining algorithm and generate a tree
        res = make_cladogram(copy.deepcopy(some))

        # Output the tree in text format to a file in the output directory. This
        # is useful when comparing if any changes have occurred during small
        # updates
        with open("output/tree_" + folder + '.txt' , 'w') as file:
            file.write('{}'.format(res))

        # Output the actual image of the NJ version of the cladogram
        output_tree.output_tree(res, folder, 'output/' + folder + '.png')

        tree = BranchAndLeafTree(res, some)
        tree.branch_swapping()
        clad = tree.to_cladogram()

        with open("output/tree_bs_" + folder + '.txt' , 'w') as file:
            file.write('{}'.format(clad))

        output_tree.output_tree(clad, folder, 'output/bs_' + folder + '.png')


if __name__ == '__main__':
    main()
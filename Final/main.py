import os
from upgma import make_dist_dict
from neighbor_joining import make_cladogram, calculateAverageD, calculate_dist_dict
from fasta import readFASTAFile
from distance import dJC
from dp_distance import dp_distance as dp_dist
import output_tree
import json, re

filename_re = re.compile(r'\w+_([\w_]+)\.fa')
def parse_filename(filename):
    return filename_re.match(filename).group(1)

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

        print(folder, [len(genes[a]) for a in genes])

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
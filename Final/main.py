import os
from upgma import make_dist_dict
from neighbor_joining import make_cladogram, calculateAverageD, calculate_dist_dict
from fasta import readFASTAFile
from distance import dJC
from dp_distance import dp_distance as dp_dist
import output_tree
import pickle, re

filename_re = re.compile(r'\w+_([\w_]+)\.fa')
def parse_filename(filename):
    return filename_re.match(filename).group(1)

def main():
    conversions = {
        "scutatus": "snake",
        "carolinensis": "lizard",
        "picta": "turtle",
        "mississippiensis": "croc",
        "platyrhynchos": "duck",
        "guttatus": "tinamou",
        "guttata": "songbird",
    }

    for folder in os.listdir('sequences'):
        genes = {}
        for filename in os.listdir('sequences/' + folder):
            name = conversions[parse_filename(filename)]
            readFASTAFile("sequences/" + folder + "/" + filename, 
                name, genes)

        print([len(genes[a]) for a in genes])

        some = make_dist_dict(genes, dp_dist)

        # print(some.keys())

        res = make_cladogram(some)

        with open("output/tree_" + folder + '.txt' , 'w') as file:
            file.write('{}'.format(res))

        output_tree.output_tree(res, folder, 'output/' + folder + '.png')


if __name__ == '__main__':
    main()
import os
from upgma import make_dist_dict
from neighbor_joining import make_cladogram, calculateAverageD, calculate_dist_dict
from fasta import readFASTAFile
from distance import dJC
from dp_distance import dp_distance as dp_dist
import output_tree
import pickle, json

def main():
    genes = {}
    for filename in os.listdir('sequences/EEF2'):
        readFASTAFile("sequences/EEF2/" + filename, genes)

    print([len(genes[a]) for a in genes])

    some = make_dist_dict(genes, dp_dist)

    with open('dist.txt', 'wb') as file:
        file.write(pickle.dumps(some))

    # with open('dist.txt', 'rb') as file:
    #     some = pickle.loads(file.read())

    print(some.keys())

    res = make_cladogram(some)

    with open("out-tree.txt", 'w') as file:
        file.write('{}'.format(res))

    output_tree.output_tree(res, "EEF2.png")


if __name__ == '__main__':
    main()
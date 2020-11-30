import os
from upgma import make_dist_dict
from neighbor_joining import make_cladogram, calculateAverageD, calculate_dist_dict
from fasta import readFASTAFile
from distance import dJC, dp_distance


def main():
    genes = {}
    readFASTAFile("sequences/EEF2/EEF2_A_carolinensis.fa", genes)
    readFASTAFile("sequences/EEF2/EEF2_A_mississippiensis.fa", genes)

    print([len(genes[a]) for a in genes])

    some = make_dist_dict(genes, dp_distance)
    print(some)


if __name__ == '__main__':
    main()
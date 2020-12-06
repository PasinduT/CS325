import math
import numpy as np
from functools import reduce

# This is the basic distance method that compares two sequences and 
# gets the fraction of sites that differ. Note that the two sequences must 
# be of equal length
# seq1: the first sequence
# seq2: the second sequence
def D (seq1, seq2):
    assert len(seq1) == len(seq2)
    diff = reduce(lambda d, x: d+(1 if x[0] != x[1] else 0), zip(seq1, seq2), 0)
    return diff / len(seq1)

    
# This function returns the Jukes-Cantor distance between two equal length
# sequences
# seq1: the first sequence
# seq2: the second sequence
def dJC (seq1, seq2):
    d = D(seq1, seq2)
    assert d < 0.75
    return -0.75 * math.log(1 - (4 * d / 3))

# This function calculates the minimum distance between two sequences
# using a dynamic programming method
# TODO: Update the gap, mismatch, and match penalties
# @deprecated use the C++ extension instead
def dp_distance(seq1, seq2):
    gap_p = 1
    mis_p = 1
    mat_b = 0

    n = len(seq1)
    m = len(seq2)

    table = np.zeros((n+1, m+1), dtype=np.int32)

    for i in range(1, n+1):
        table[i][0] = table[i-1][0] + gap_p

    for i in range(1, m+1):
        table[0][i] = table[0][i-1] + gap_p

    for i in range(1, n+1):
        for j in range(1, m+1):
            if seq1[i-1] == seq2[j-1]:
                table[i][j] = table[i-1][j-1] + mat_b
            else:
                table[i][j] = min(table[i-1][j] + gap_p, 
                    min(table[i][j-1] + gap_p, table[i-1][j-1]) + mis_p)
    # print(table)
    return table[n][m]

def test():
    seq1 = "ATARA"
    seq2 = "ATATT"

    print(dp_distance(seq1, seq2))

    print(D(seq1, seq2))

if __name__ == '__main__':
    test()
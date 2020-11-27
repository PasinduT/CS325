import math

# This is the basic distance method that compares two sequences and 
# gets the fraction of sites that differ. Note that the two sequences must 
# be of equal length
def D (seq1, seq2):
    assert len(seq1) == len(seq2)
    differ = 0
    for a, b in zip(seq1, seq2):
        if a != b:
            differ += 1

    ans = differ / len(seq1)
    assert ans < 0.75
    return ans

# This function returns the Jukes-Cantor distance
# between two sequence
# seq1: the first sequence
# seq2: the second sequence
def dJC (seq1, seq2):
    return -0.75 * math.log(1 - (4 * D(seq1, seq2) / 3))
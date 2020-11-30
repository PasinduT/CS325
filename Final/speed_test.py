from dp_distance import dp_distance as dp_c
from distance import dp_distance as dp_python
from fasta import readFASTAFile
from timeit import default_timer as timer

def test():
    genes = {}

    readFASTAFile("sequences/EEF2/EEF2_A_carolinensis.fa", "some", genes)
    readFASTAFile("sequences/EEF2/EEF2_A_mississippiensis.fa", "other", genes)


    keys = list(genes.keys())
    first = genes[keys[0]]
    second = genes[keys[1]]

    print("The sequences are {} and {} long".format(len(first), len(second)))

    start = timer()
    c_version = dp_c(first, second)
    end = timer()
    c_time = end - start

    start = timer()
    py_version = dp_c(first, second)
    end = timer()
    py_time = end - start

    print("The distance calculated using C version:\t{}".format(c_version))
    print("The distance calculated using Python version:\t{}".format(py_version))
    print("Time taken by C version:     ", c_time)
    print("Time taken by Python version:", py_time)

if __name__ == '__main__':
    test()

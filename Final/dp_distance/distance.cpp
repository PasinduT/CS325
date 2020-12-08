#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <string.h>
#include <algorithm>
using namespace std;

/**
 * This function calculates the distance between two DNA sequences. Since the 
 * function is called using Python, the arguments are passed as a python tuple
 * which is parsed. In this function, gaps are penalized as +4 each, transitions
 * are penalized as +1 each, and tranversions are penalized as +2 each.
 * self: the object to which this object belongs
 * args: the arguments passed on to the function
 * Return: the distance between two DNA sequences.
 */
static PyObject * dp_distance(PyObject * self, PyObject * args) {
    // Initialize the penalties
    const int transition_penalty = 1;
    const int transversion_penalty = 2;
    const int gap_penalty = 4;

    // Char pointers to point to the DNA sequences
    const char * s1;
    const char * s2;
    
    // Extract the two sequences from the Python tuple of arguments
    PyArg_ParseTuple(args, "ss", &s1, &s2);

    // Get the length of the sequences
    uint n = strlen(s1);
    uint m = strlen(s2);
    
    // Make two sequences that will hold the memoized values from the dynamic
    // programming algorithm. Note that only two rows of the matrix are needed
    // since we only need the distance and not the entire distance
    uint *previous = new uint[(m+1)];
    uint *next = new uint[(m+1)];
    
    // Initialize the first row of the matrix.
    previous[0] = 0;
    for (uint i = 1; i < m+1; ++i) previous[i] = previous[i-1] + gap_penalty;

    // Start from the second row of the matrix and continue until the final 
    // distance (the last entry in the matrix) has been calculated.
    for (uint i = 1; i < n+1; ++i) {
        next[0] = i * gap_penalty;
        for (uint j = 1; j < m+1; ++j) {
            // If they match, then there would be no penalty.
            if (s1[i-1] == s2[j-1]) {
                next[j] = previous[j-1];
            }
            else {
                // Otherise calculate the penalty
                register int penalty = s1[i-1] ^ s2[j-1];

                // If the mismatch is a transition
                if (penalty == 6 || penalty == 23) penalty = transition_penalty;
                // If the mismatch is a transversion penalty.
                else penalty = transversion_penalty;

                // Choose the minimum penalty for this entry in the matrix and 
                // store it
                next[j] = min(previous[j-1] + penalty, 
                    min(previous[j-1], 
                        previous[j]) + gap_penalty);
            }
        }
        // Swap the pointers of previous and next, so that the previous row 
        // becomes the next row, and the next row becomes the previous row
        swap(previous, next);
    }
    // Store the final result in a variable and perform memory management
    int result = previous[m];
    delete [] previous;
    delete [] next;    

    // Return the result
    return PyLong_FromLong(result);
}

// These are the boilerplate structs and methods needed to implement a C++ 
// extension to Python
static PyMethodDef distance_methods[] = {
    {"dp_distance", dp_distance, METH_VARARGS, 
        "Implements edit distance between two sequences"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef distance_module = {
    PyModuleDef_HEAD_INIT,
    "dp_distance",
    "Implements edit distance between two sequences",
    -1,
    distance_methods
};

PyMODINIT_FUNC PyInit_dp_distance(void) {
    return PyModule_Create(&distance_module);
}


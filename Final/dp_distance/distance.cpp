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
    uint *old = new uint[(m+1)];
    uint *later = new uint[(m+1)];
    
    // Initialize the first row of the matrix.
    old[0] = 0;
    for (uint i = 1; i < m+1; ++i) old[i] = old[i-1] + 4;

    // Start from the second row of the matrix and continue until the final 
    // distance (the last entry in the matrix) has been calculated.
    for (uint i = 1; i < n+1; ++i) {
        later[0] = i * 4;
        for (uint j = 1; j < m+1; ++j) {
            // If they match, then there would be no penalty.
            if (s1[i-1] == s2[j-1]) {
                later[j] = old[j-1];
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
                later[j] = min(old[j-1] + penalty, 
                    min(old[j-1], 
                        old[j]) + gap_penalty);
            }
        }
        // Swap the pointers of old and later, so that the old row becomes the 
        // new row, and the new row becomes the old row
        swap(old, later);
    }
    // Store the final result in a variable and perform memory management
    int result = old[m];
    delete [] old;
    delete [] later;    

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


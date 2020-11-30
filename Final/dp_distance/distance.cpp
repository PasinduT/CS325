#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <string.h>
#include <algorithm>
using namespace std;


static PyObject * dp_distance(PyObject * self, PyObject * args) {
    const char * s1;
    const char * s2;

    int k = PyArg_ParseTuple(args, "ss", &s1, &s2);

    int n = strlen(s1);
    int m = strlen(s2);
    

    int *old = new int[(m+1)];
    int *later = new int[(m+1)];

    // cout << "Got here" << endl;
    
    old[0] = 0;
    for (int i = 1; i < m+1; ++i) old[i] = old[i-1] + 1;


    // cout << "and here" << endl;

    for (int i = 1; i < n+1; ++i) {
        later[0] = i;
        for (int j = 1; j < m+1; ++j) {
            if (s1[i-1] == s2[j-1]) {
                later[j] = old[j-1];
            }
            else {
                later[j] = min(old[j-1] + 1, 
                    min(old[j-1] + 1, 
                        old[j]+ 1));
            }
        }
        int *temp = old;
        old = later;
        later = temp;
    }

    int val = old[m];
    delete [] old;
    delete [] later;    

    return PyLong_FromLong(val);
}

static PyMethodDef distance_methods[] = {
    {"dp_distance", dp_distance, METH_VARARGS, "Implements edit distance between two sequences"},
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


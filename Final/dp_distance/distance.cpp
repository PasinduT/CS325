#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <string.h>
#include <algorithm>
using namespace std;


static PyObject * dp_distance(PyObject * self, PyObject * args) {
    const char * s1;
    const char * s2;

    PyArg_ParseTuple(args, "ss", &s1, &s2);

    uint n = strlen(s1);
    uint m = strlen(s2);
    

    uint *old = new uint[(m+1)];
    uint *later = new uint[(m+1)];
    
    old[0] = 0;
    for (uint i = 1; i < m+1; ++i) old[i] = old[i-1] + 4;

    for (uint i = 1; i < n+1; ++i) {
        later[0] = i * 4;
        for (uint j = 1; j < m+1; ++j) {
            if (s1[i-1] == s2[j-1]) {
                later[j] = old[j-1];
            }
            else {
                register int val = s1[i-1] ^ s2[j-1];
                if (val == 6 || val == 23) val = 1;
                else val = 2;

                later[j] = min(old[j-1] + val, 
                    min(old[j-1] + 4, 
                        old[j]+ 4));
            }
        }
        swap(old, later);
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


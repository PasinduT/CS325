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

    
    int *table = new int[(n+1) * (m+1)];
    table[0] = 0;

    for (int i = 1; i < n+1; ++i) table[i * (m+1)] = table[(i-1) * (m+1)] + 1;
    for (int i = 1; i < m+1; ++i) table[i] = table[i-1] + 1;

    for (int i = 1; i < n+1; ++i) {
        for (int j = 1; j < m+1; ++j) {
            if (s1[i-1] == s2[j-1]) {
                table[(i * (m+1)) + j] = table[((i-1) * (m+1)) + (j-1)];
            }
            else {
                table[(i * (m+1)) + j] = min(table[((i-1) * (m+1)) + (j-1)] + 1, 
                    min(table[((i) * (m+1)) + (j-1)] + 1, 
                        table[((i-1) * (m+1)) + j]+ 1));
            }
        }
    }

    int val = table[(n * (m+1)) + m];
    delete [] table;    

    return PyLong_FromLong(val);
}

static PyMethodDef distance_methods[] = {
    {"dp_distance", dp_distance, METH_VARARGS, "Something much ado about nothing"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef distance_module = {
    PyModuleDef_HEAD_INIT,
    "dp_distance",
    "something much ado about nothing",
    -1,
    distance_methods
};

PyMODINIT_FUNC PyInit_dp_distance(void) {
    return PyModule_Create(&distance_module);
}


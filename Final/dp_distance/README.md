# DP Distance C++ extension for Python

To use this library, you have to first compile and install it.
You can use 

`python3 setup.py build`

and then you will find the compiled library in the build/ directory. At which 
point you need to copy over the library to the python working directory. 
For example, by using the command:

`cp build/*/*.so ..`

A Makefile is included which simplifies this task. You can run it by using

`make clean && make`

or, if you are in a MacOS environment,

`make clean && make mac`
# Final Project

`main.py` is the starting point for this program. It can be run using

`python3 main.py`

All the trees generated can be found in the output/ directory. To avoid running 
the dp_distance algorithm. The results of the algorithm are cached in the 
output/distances directory as .json files. To rerun the dp_distance algorithm,
simply delete all those .json files and run `main.py` 

## Requirements

- ETE library
    
    `pip install ete3`
    
- dp_distance library - you can compile it for a linux system using (Cython):

    `cd dp_distance && make clean && make`

    or, if you are on a mac:

    `cd dp_distance && make clean && make mac`

## Generated trees

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/EEF2.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/TPM1.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/myogoblin.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/NTF3.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/RHO.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/bs_EEF2.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/bs_TPM1.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/bs_myogoblin.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/bs_NTF3.png)

![](https://raw.githubusercontent.com/PasinduT/CS325/master/Final/output/bs_RHO.png)

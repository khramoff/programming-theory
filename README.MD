# Theorems

This program is used to prove some theorems from programming theory:
1. Superposition of functions (programs)
1. Minimization of function
1. Primitive recursion

## Running
Program accepts 3 arguments
* input file - file that contains all nessessary info
* output file - file to put result to 
* command - either `r`, `s` or `m`

##  Minimization
Input file structure
```
n
function_to_minimize.urm
```

Runnign:
```bash
python3 main.py -command=m -i input.txt -o output.urm
```

##  Recursion
Input file structure
```
n
f.urm
g.urm
```

Runnign:
```bash
python3 main.py -command=r -i input.txt -o output.urm
```


##  Superposition
Input file structure
```
n
k
f.urm
g1.urm
...
gk.urm
```

Runnign:
```bash
python3 main.py -command=s -i input.txt -o output.urm
```


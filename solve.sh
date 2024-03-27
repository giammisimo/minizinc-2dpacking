#!/bin/bash

## MiniZincIDE path - The following script uses an IDE installation
## (It can be modified to work with a normal CLI installation)
MZN_IDE_DIR=$(cat ./ide_path)

MINIZINC=$MZN_IDE_DIR/bin/minizinc
export MZN_STDLIB_DIR=$MZN_IDE_DIR/share/minizinc/


## The solver configuration is the same as the example provided here:
## https://www.minizinc.org/doc-2.5.5/en/installation_detailed_linux.html#gecode
## The <INSTALLATION_PREFIX> in this case is MZN_IDE_DIR

$MINIZINC --solver gecode.msc ./2dpacking_intervals.mzn example.dzn | tee sol.txt
python3 plot.py

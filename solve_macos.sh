#!/bin/bash
## The solver configuration is the same as the example provided here:
## https://www.minizinc.org/doc-2.5.5/en/installation_detailed_linux.html#gecode
## The <INSTALLATION_PREFIX> in this case is MZN_IDE_DIR

minizinc --solver Gecode ./2dpacking_intervals.mzn example.dzn | tee sol.txt
python3.12 plot.py

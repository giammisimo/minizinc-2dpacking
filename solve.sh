#!/bin/bash

#!/bin/bash
## The solver configuration is the same as the example provided here:
## https://www.minizinc.org/doc-2.5.5/en/installation_detailed_linux.html#gecode
## The <INSTALLATION_PREFIX> in this case is MZN_IDE_DIR

# Check current operating system
OS=$(uname)

if [[ "$OS" == "Linux" ]]; then
    # Percorso di MiniZincIDE su Linux
    MZN_IDE_DIR=$(cat ./ide_path)
    MINIZINC=$MZN_IDE_DIR/bin/minizinc
    export MZN_STDLIB_DIR=$MZN_IDE_DIR/share/minizinc/

    $MINIZINC --solver gecode.msc ./2dpacking_intervals.mzn example.dzn | tee sol.txt
    python3 plot.py

elif [[ "$OS" == "Darwin" ]]; then
    minizinc --solver Gecode ./2dpacking_intervals.mzn example.dzn | tee sol.txt
    python3.12 plot.py
else
    echo "Sistema operativo non supportato"
    exit 1
fi

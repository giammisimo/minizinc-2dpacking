# 2D Packing
Project for the "Constraint Programming" Course @ University of Parma

This project requires python-tk and a  minizinc solver.

## On MacOS

Export the path of the minizinc IDE in the PATH variable

```bash
export PATH=/Applications/MiniZincIDE.app/Contents/Resources:$PATH
```

How to run the project:

```bash
python run_bench.py 2dpacking_intervals.mzn
python3.12 plot.py benchmarks-results/bench19-10.txt
```
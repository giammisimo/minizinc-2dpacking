# 2D Packing
Project for the "Constraint Programming" Course @ University of Parma

This project is based on the Minizinc constraint modeling language.
The specification of the problem can be found in `specification.md`.

## On MacOS

Export the path of the minizinc IDE in the PATH variable

```bash
export PATH=/Applications/MiniZincIDE.app/Contents/Resources:$PATH
```

How to run the project:

```bash
python run_bench.py 2dpacking_intervals.mzn
```

## Visualization

There are a few tools to visualize the results of the model.
`plot.py` and `show-gist.py` show the result for gecode/chuffed and gist respectively.
For these scripts, the `matplotlib` library is needed.

There is also a web-app that serves these two scripts in the `web/` directory based on Docker.
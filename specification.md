# 2D Packing
A number of boxes with size $x \times y$ must be loaded on a pallet of size $k \times k$. 
Boxes can be placed so that no boxes overlap and no boxes overflow the pallet. 
Boxes can be rotated by 90 degrees and they have one side that is parallel to one pallet’s side. Assume to work with integer coordinates.
The problem goal is to maximize the number of boxes that can be loaded on the pallet and to produce an arrangement in the 2D space.

1. Write a Minizinc program capable of finding the optimal solution.
2. Prepare a battery of benchmark instances in the following way: $x = 5, 10, 15, 20$ and $y = x+5$ box size and $k = 20 − 1, 30 − 1, . . . , 100 − 1$. (36 instances in total)
3. Run your Minizinc encoding on all the instances, possibly exploring different search strategies, with a timeout of 5 minutes for each test (“configuration” option in Minizinc) Report the best value for the solution found within the timeout.
4.  Write a 6–10 pages report containing your models (and the reasons for some choices) and a presentation of the execution results. Prepare the programs and the benchmark instances used in a unique zip file.
include "globals.mzn";

int: k = 19;
int: x = 5;
int: y = x + 5;
int: n = 4;%(k*k) div (x*y); %upper bound

% Position of the upper-left corner of every box
array [1..n,1..2] of var 1..k: positions; 
% Sizes for every box
array [1..n,1..2] of var {x,y}: sizes; 
var 0..n: boxes;

% x != y in sizes
constraint forall(i in 1..n)(
  sizes[i,1] != sizes[i,2]
);

% the boxes' corner must be inside the pallet
constraint forall(i in 1..n)(
  positions[i,1] > 0 /\ positions[i,1] <= k /\
  positions[i,2] > 0 /\ positions[i,2] <= k
);

%every box must be inside the pallet
constraint forall(i in 1..n)(
  positions[i,1] + sizes[i,1] <= k /\
  positions[i,2] + sizes[i,2] <= k
);

%the boxes must not overlap
constraint diffn_k(positions, sizes);

solve satisfy;

output [
  "x: ", show(x), "\ny: " , show(y), "\nk: ", show(k), "\nn: ", show(n), "\n***\n",
  "positions:"
]
++
[if j = 1 then "\n" endif ++
  show(positions[i,j]) ++ "," | i in 1..n, j in 1..2
]
++["\n***\nsizes:"]++
[if j = 1 then "\n" endif ++
  show(sizes[i,j]) ++ "," | i in 1..n, j in 1..2
] ++ ["\n***\nboxes: ", show(boxes)]
;
% symmetry breaking
% 1. One box must have a corner at the origin
% 2. Every box must touch another one
% 3. Boxes are ordered in position based on index

include "globals.mzn";
int: k;         % Size of the pallet
int: x; int: y; % Dimensions of the boxes
int: n = (k*k) div (x*y); % Upper bound for the boxes

array [1..n,1..2] of var 1..k: positions; % Position of the 
                                          % upper-left corner 
                                          % of every box
array [1..n,1..2] of var {x,y}: sizes; % Sizes for every box
var 1..n: boxes; % Number of boxes

% Respect box size in rotation
constraint forall(i in 1..boxes)(
  sizes[i,1] != sizes[i,2] \/ x = y
);

% The boxes must not overflow the pallet
constraint forall(i in 1..boxes)(
  positions[i,1] + sizes[i,1] <= k + 1 /\
  positions[i,2] + sizes[i,2] <= k + 1
);

% The boxes must not overlap
constraint diffn_k(positions, sizes);

solve maximize boxes;

output [
  "x: ", show(x), "\ny: " , show(y), "\nk: ", show(k), "\nn: ", show(n), "\n***\n",
  "positions:"
]
++
[if j = 1 then "\n" else "" endif ++
  show(positions[i,j]) ++ "," | i in 1..n, j in 1..2
]
++["\n***\nsizes:"]++
[if j = 1 then "\n" else "" endif ++
  show(sizes[i,j]) ++ "," | i in 1..n, j in 1..2
] ++ ["\n***\nboxes: ", show(boxes)];
include "globals.mzn";

int: k; % = 19;
int: x; % = 5;
int: y = x + 5;
int: n = (k * k) div (x * y); % upper bound

% Position of the upper-left corner of every box
array [1..n, 1..2] of var 1..k: positions;
% Sizes for every box
array [1..n, 1..2] of var {x, y}: sizes;
var 0..n: boxes;

% x != y in sizes
constraint forall(i in 1..boxes)(
  sizes[i, 1] != sizes[i, 2]
);

% the boxes' corner must be inside the pallet
constraint forall(i in 1..boxes)(
  positions[i, 1] > 0 /\ positions[i, 1] <= k /\
  positions[i, 2] > 0 /\ positions[i, 2] <= k
);

% every box must be inside the pallet
constraint forall(i in 1..boxes)(
  positions[i, 1] + sizes[i, 1] - 1 <= k /\
  positions[i, 2] + sizes[i, 2] - 1 <= k
);

% the boxes must not overlap
constraint forall(i in 1..boxes, j in i+1..boxes) (
  (positions[i,1] + sizes[i,1] - 1 < positions[j,1] \/
   positions[j,1] + sizes[j,1] - 1 < positions[i,1] \/
   positions[i,2] + sizes[i,2] - 1 < positions[j,2] \/
   positions[j,2] + sizes[j,2] - 1 < positions[i,2])
);

% Symmetry breaking 1: The first box must be at the origin (1,1)
constraint positions[1,1] = 1 /\ positions[1,2] = 1;

solve maximize boxes;

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

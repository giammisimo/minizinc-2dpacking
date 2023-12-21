include "globals.mzn";

int: k = 19;
int: x = 5;
int: y = x + 5;
int: n = 4;%(k*k) div (x*y); %upper bound

%array[1..k,1..k] of var 0..n: grid;
array [1..n,1..2] of var 1..k: positions; 
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

% symmetry breaking
% 1. One box must have a corner at the origin
% 2. Every box must touch another one

include "globals.mzn";

int: k;        % Size of the pallet
int: x; int: y;% Dimensions of the boxes
int: n = (k*k) div (x*y); % Upper bound for the boxes

function int: gcd(int: a, int: b) = 
  let {
    int: abs_a = abs(a);
    int: abs_b = abs(b);
  } in
  if abs_b == 0 then abs_a
  else gcd(abs_b, abs_a mod abs_b)
  endif;

int: modulo = gcd(x, y);

% Position of the upper-left corner of every box
array [1..n,1..2] of var {1 + modulo * t | t in 0..(k div modulo)}: positions; 
% Sizes for every box
array [1..n,1..2] of var {x,y}: sizes; 
var 1..n: boxes;

% x != y in sizes
constraint forall(i in 1..boxes)(
  sizes[i,1] != sizes[i,2] \/ x = y
);

% the boxes' corner must be inside the pallet
constraint forall(i in 1..boxes)(
  positions[i,1] > 0 /\ positions[i,1] <= k /\
  positions[i,2] > 0 /\ positions[i,2] <= k
);

%every box must be inside the pallet
constraint forall(i in 1..boxes)(
  positions[i,1] + sizes[i,1] <= k + 1 /\
  positions[i,2] + sizes[i,2] <= k + 1
);

%the boxes must not overlap
constraint diffn_k(positions, sizes);

% Symmetry breaking 1: The first box must be at the origin (1,1) and is horizontal
constraint (
  positions[1,1] = 1 /\ positions[1,2] = 1 /\
  sizes[1,1] = max(x,y) /\ sizes[1,2] = min(x,y)
);

% Symmetry breaking 2: Order the positions
constraint lex2(positions);


solve :: seq_search([
             int_search(positions, input_order, indomain_min),int_search(sizes, input_order, indomain_max)])
      maximize boxes;

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
] ++ ["\n***\nboxes: ", show(boxes)]
;
% symmetry breaking
% 1. One box must have a corner at the origin
% 2. Every box must touch another one
% 3. Boxes are ordered in position based on index
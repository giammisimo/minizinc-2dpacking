%-----------------------------------------------------------------------------
% 2D Packing Problem using Intervals
% This model solves a 2D bin packing problem where we need to place rectangular
% boxes of size x×y into a square pallet of size k×k, maximizing the number of
% placed boxes.
%-----------------------------------------------------------------------------

% Global constraints inclusion
include "globals.mzn";

%-----------------------------------------------------------------------------
% Input Parameters
%-----------------------------------------------------------------------------
int: k;        % Size of the square pallet (k×k)
int: x; int: y;% Dimensions of the boxes (x×y or y×x as they can be rotated)
int: n = (k*k) div (x*y); % Upper bound for the number of boxes that can fit

%-----------------------------------------------------------------------------
% Helper Functions
%-----------------------------------------------------------------------------
% GCD function used to determine possible positions
function int: gcd(int: a, int: b) = 
  let {
    int: abs_a = abs(a);
    int: abs_b = abs(b);
  } in
  if abs_b == 0 then abs_a
  else gcd(abs_b, abs_a mod abs_b)
  endif;

int: modulo = gcd(x, y);

%-----------------------------------------------------------------------------
% Decision Variables
%-----------------------------------------------------------------------------
% positions[i,1..2]: Coordinates of the upper-left corner of box i
% Values are restricted to multiples of modulo + 1 to reduce search space
array [1..n,1..2] of var {1 + modulo * t | t in 0..(k div modulo)}: positions; 

% sizes[i,1..2]: Width and height of box i (can be rotated: x,y or y,x)
array [1..n,1..2] of var {x,y}: sizes; 

% Number of boxes we actually place (this is what we maximize)
var 1..n: boxes;

%-----------------------------------------------------------------------------
% Constraints
%-----------------------------------------------------------------------------
% Ensure proper dimensions when x ≠ y (rotation constraint)
constraint forall(i in 1..boxes)(
  sizes[i,1] != sizes[i,2] \/ x = y
);

% Ensure boxes are placed within pallet boundaries
constraint forall(i in 1..boxes)(
  positions[i,1] > 0 /\ positions[i,1] <= k /\
  positions[i,2] > 0 /\ positions[i,2] <= k
);

% Ensure boxes don't exceed pallet boundaries
constraint forall(i in 1..boxes)(
  positions[i,1] + sizes[i,1] <= k + 1 /\
  positions[i,2] + sizes[i,2] <= k + 1
);

% Prevent box overlapping using the diffn_k global constraint
constraint diffn_k(positions, sizes);

%-----------------------------------------------------------------------------
% Symmetry Breaking Constraints
%-----------------------------------------------------------------------------
% Symmetry Breaking 1 and 2: Force first box placement and orientation
% - Places the first box at position (1,1)
% - Forces horizontal orientation (longer side horizontal)
% This eliminates rotational and translational symmetry for the first box
constraint (
  positions[1,1] = 1 /\ positions[1,2] = 1 /\
  sizes[1,1] = max(x,y) /\ sizes[1,2] = min(x,y)
);

% Symmetry Breaking 3: Lexicographic ordering of positions
% Forces a total order on box positions to eliminate equivalent solutions
% where boxes are just reindexed
constraint lex2(positions);

%-----------------------------------------------------------------------------
% Search Strategy and Objective
%-----------------------------------------------------------------------------
solve :: seq_search([
             int_search(positions, input_order, indomain_min),
             int_search(sizes, input_order, indomain_max)])
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
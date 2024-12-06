include "globals.mzn";

int: k;% = 19;
int: x;% = 5;
int: y;% = x + 5;
int: n = (k*k) div (x*y); %upper bound

% Position of the upper-left corner of every box
array [1..n,1..2] of var 1..k: positions; 
% Sizes for every box
array [1..n,1..2] of var {x,y}: sizes; 
var 0..n: boxes;
array[1..n, 1..n] of var bool: adjacency; 

% x != y in sizes
constraint forall(i in 1..boxes)(
  sizes[i,1] != sizes[i,2]
);

% the boxes' corner must be inside the pallet
constraint forall(i in 1..boxes)(
  positions[i,1] > 0 /\ positions[i,1] <= k /\
  positions[i,2] > 0 /\ positions[i,2] <= k
);

%every box must be inside the pallet
constraint forall(i in 1..boxes)(
  positions[i,1] + sizes[i,1] <= k /\
  positions[i,2] + sizes[i,2] <= k
);

%the boxes must not overlap
%constraint diffn_k(positions, sizes);
%this constraint generates much fewer subtrees
constraint forall(i in 1..boxes, j in i+1..boxes) (
  (positions[i,1] + sizes[i,1] - 1 < positions[j,1] \/
   positions[j,1] + sizes[j,1] - 1 < positions[i,1] \/
   positions[i,2] + sizes[i,2] - 1 < positions[j,2] \/
   positions[j,2] + sizes[j,2] - 1 < positions[i,2])
);

% Symmetry breaking 1: The first box must be at the origin (1,1)
constraint positions[1,1] = 1 /\ positions[1,2] = 1;

% Symmetry breaking 2: The coordinates are always 1 mod 5
%constraint forall(i in 1..boxes)(
  % More case specific
  %positions[i,1] mod 5 = 1 /\ 
  %positions[i,2] mod 5 = 1
  % More general
%  (positions[i,1] mod x = 1 \/ positions[i,1] mod y = 1) /\ 
%  (positions[i,2] mod x = 1 \/ positions[i,2] mod y = 1)
%);

% Symmetry breaking 3: The boxes at x = 0 are horizontal
constraint sizes[1,1] = max(x,y) /\ sizes[1,2] = min(x,y);

% Symmetry breaking 4: Order the positions
constraint forall(i in 1..boxes, j in i+1..boxes) (
  ((positions[i,1]-1) * k + (positions[i,2]-1)) <= 
  ((positions[j,1]-1) * k + (positions[j,2]-1))
);

constraint forall(i in boxes+1..n) (
  positions[i,1] = k /\ positions[i,2] = k /\
  sizes[i,1] = x /\ sizes[i,2] = y
);

predicate edge_exists(int: u, int: v) =
    (u != v) /\ (u <= boxes /\ v <= boxes) /\ (
      (positions[u,1] + sizes[u,1] = positions[v,1] /\
       ((positions[u,2] >= positions[v,2] /\ positions[u,2] < (positions[v,2] + sizes[v,2])) \/
        (positions[v,2] >= positions[u,2] /\ positions[v,2] < (positions[u,2] + sizes[u,2])))) \/ 
      (positions[u,2] + sizes[u,2] = positions[v,2] /\ 
       ((positions[u,1] >= positions[v,1] /\ positions[u,1] < (positions[v,1] + sizes[v,1])) \/
        (positions[v,1] >= positions[u,1] /\ positions[v,1] < (positions[u,1] + sizes[u,1]))))
    );
    
  
constraint
    forall(u in 1..boxes, v in 1..boxes where u < v) (
        adjacency[u, v] = edge_exists(u, v)
    );
    
constraint forall(u in 1..boxes, v in 1..boxes)( 
  adjacency[v, u] = adjacency[u, v]
);

constraint forall(u in 1..n, v in 1..n)( 
  (u > boxes \/ v > boxes \/ u = v) -> (adjacency[u,v] = false)
);
    
constraint forall(i in 1..boxes)(
  %exists([adjacency[i,j] | j in 1..boxes])
  sum([adjacency[i,j] | j in 1..boxes]) > 2
);


int:sol;
constraint boxes = sol;

solve :: seq_search([
             %int_search([boxes], first_fail, indomain_min),int_search(positions, input_order, indomain_min)])
             int_search(positions, input_order, indomain_min), int_search([boxes], first_fail, indomain_min)])
      satisfy;

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
++["\n***\nadj:"]++
[if j = 1 then "\n" else "" endif ++
  show(adjacency[i,j]) ++ "," | i in 1..n, j in 1..n
]
;
% symmetry breaking
% 1. One box must have a corner at the origin
% 2. Every box must touch another one
% 3. Boxes are ordered in position based on index

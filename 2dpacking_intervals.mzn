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
var 0..n: boxes;

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
%constraint diffn_k(positions, sizes);
%diffn for 2 dimensions
constraint forall(i in 1..boxes, j in 1..boxes where i < j) (
  (positions[i,1] + sizes[i,1] - 1 < positions[j,1] \/
   positions[j,1] + sizes[j,1] - 1 < positions[i,1] \/
   positions[i,2] + sizes[i,2] - 1 < positions[j,2] \/
   positions[j,2] + sizes[j,2] - 1 < positions[i,2])
);

% Symmetry breaking 1: The first box must be at the origin (1,1) and is horizontal
constraint (
  positions[1,1] = 1 /\ positions[1,2] = 1 /\
  sizes[1,1] = max(x,y) /\ sizes[1,2] = min(x,y)
);

% Symmetry breaking 2: Order the positions
%constraint forall(i in 1..boxes, j in 1..boxes where i < j) (
%  ((positions[i,1]-1) * k + (positions[i,2]-1)) <= 
%  ((positions[j,1]-1) * k + (positions[j,2]-1))
%);

constraint lex2(positions);

% All spare values that do not represent a box are defaulted
%constraint forall(i in boxes+1..n) (
%  positions[i,1] = k /\ positions[i,2] = k /\
%  sizes[i,1] = x /\ sizes[i,2] = y
%);

% Predicate: Check if two boxes are adjacent
predicate edge_exists(int: u, int: v) =
    (u != v) /\ (u <= boxes /\ v <= boxes) /\ (
      (positions[u,1] + sizes[u,1] = positions[v,1] /\
       ((positions[u,2] >= positions[v,2] /\ positions[u,2] < (positions[v,2] + sizes[v,2])) \/
        (positions[v,2] >= positions[u,2] /\ positions[v,2] < (positions[u,2] + sizes[u,2])))) \/ 
      (positions[u,2] + sizes[u,2] = positions[v,2] /\ 
       ((positions[u,1] >= positions[v,1] /\ positions[u,1] < (positions[v,1] + sizes[v,1])) \/
        (positions[v,1] >= positions[u,1] /\ positions[v,1] < (positions[u,1] + sizes[u,1]))))
    );
    
% The adjacency matrix for the graph
%array[1..n, 1..n] of var bool: adjacency;  

% The adjacency matrix must be symmetric, if u is adjacent to v, then v is adjacent to u
%constraint
%    forall(u in 1..n, v in 1..n where u < v) (
%        adjacency[u, v] = edge_exists(u, v) /\
%        adjacency[v, u] = adjacency[u, v] % Ensure symmetry for undirected graph
%    );

% Not valid connections shall not be adjacent
%constraint forall(u in 1..n, v in 1..n)( 
%  (u > boxes \/ v > boxes \/ u = v) -> (adjacency[u,v] = false)
%);
    
% 
%constraint forall(i in 1..boxes)(
%  sum([adjacency[i,j] | j in 1..boxes]) > 1
%);


% If GCD is greater than 1, then the boxes must be placed at coordinates that are 1 mod GCD
%constraint forall(i in 1..boxes)(
%  modulo > 1 -> (positions[i,1] mod modulo = 1 /\ positions[i,2] mod modulo = 1 )
%);

% Predicate: Check if a point is inside a box
predicate inside_box(int: x, int: y) =
(
  exists(i in 1..boxes)(
    (x >= positions[i,1] /\ x <= positions[i,1] + sizes[i,1]) /\
    (y >= positions[i,2] /\ y <= positions[i,2] + sizes[i,2])
  )
);

% Predicate: Check if a point is a concave point
% A point is concave if it is not inside a box and its neighbors are
predicate concave_point(int: i, int: j) = (
  i > 0 /\ j > 0 /\ i < k /\ j < k /\ not inside_box(i,j) /\
  inside_box(i-1,j) /\ inside_box(i,j-1)
);

% The number of concave points must be less than 2
%constraint sum(i in 1..k, j in 1..k)(concave_point(i,j)) < 2;

%var 100..n*100: target;
%constraint target = boxes * 100 - (max([positions[i,1] | i in 1..boxes]) + max([positions[i,2] | i in 1..boxes]));
%constraint target = boxes * 100 - (sum([sizes[i,1] < sizes[i,2] | i in 1..boxes]));

%constraint sum([sizes[i,1] > sizes[i,2] | i in 1..boxes]) >= (boxes div 2);


%solve :: int_search([boxes], first_fail, indomain_min) maximize boxes;
solve :: seq_search([
             %int_search([boxes], first_fail, indomain_min),int_search(positions, input_order, indomain_min)])
             int_search(positions, input_order, indomain_min),int_search(sizes, input_order, indomain_max)])
      maximize boxes;
%solve maximize boxes;

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
%++["\n***\nadj:"]++
%[if j = 1 then "\n" else "" endif ++
%  show(adjacency[i,j]) ++ "," | i in 1..n, j in 1..n
%]
;
% symmetry breaking
% 1. One box must have a corner at the origin
% 2. Every box must touch another one
% 3. Boxes are ordered in position based on index

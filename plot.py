"""
Shows solution from Gecode.
Takes a file path as input.
To launch
python3 plot.py <solution>
"""
import sys
import matplotlib.pyplot as plt
import numpy as np

def read_solution(filename):
    """
    Read and parse the solution file
    """
    with open(filename, 'r') as f:
        solution = f.read()
    
    # Parse parameters
    parameters = solution.split('***')[0].split('\n')[:-1]
    x, y, k, n = tuple([int(par.split(' ')[1]) for par in parameters])
    
    # Parse boxes
    boxes = int(solution.split('***')[3].split('\n')[1].split(' ')[1])
    
    # Parse positions and sizes
    positions = solution.split('***')[1][len('positions:'):].split('\n')[1:-1]
    positions = [(int(pos.split(',')[0]),int(pos.split(',')[1])) for pos in positions[:boxes]]
    
    sizes = solution.split('***')[2][len('sizes:'):].split('\n')[1:-1]
    sizes = [(int(size.split(',')[0]),int(size.split(',')[1])) for size in sizes[:boxes]]
    
    return x, y, k, n, boxes, positions, sizes

def visualize_grid(x, y, k, boxes, positions, sizes):
    """
    Visualize the grid using Matplotlib
    """
    # Predefined color palette
    colors = [
        'yellow', 'red', 'green', 'blue', 'orange', 
        'purple', 'brown', 'pink', 'cyan', 'magenta'
    ]
    
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw the grid
    for i in range(k):
        for j in range(k):
            ax.add_patch(plt.Rectangle((j, k-1-i), 1, 1, 
                                       fill=False, 
                                       edgecolor='black', 
                                       linewidth=1))
    
    # Place boxes
    for idx in range(boxes):
        pos = positions[idx]
        size = sizes[idx]
        color = colors[idx % len(colors)]
        # Adjust for coordinate system (bottom-left origin)
        ax.add_patch(plt.Rectangle((pos[0]-1, pos[1]-1), 
                                   size[0], size[1], 
                                   color=color, 
                                   alpha=0.7, 
                                   edgecolor='black'))
    
    # Set plot properties
    ax.set_xlim(0, k)
    ax.set_ylim(0, k)
    ax.set_aspect('equal')
    ax.set_title(f'k={k} / x = {x} / y = {y} / boxes = {boxes}')
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    
    # Add grid labels
    plt.xticks(np.arange(0.5, k, 1), range(1, k+1))
    plt.yticks(np.arange(0.5, k, 1), range(1, k+1))
    
    return fig, ax

def main():
    # Check if filename is provided
    if len(sys.argv) < 2:
        print("Please provide a solution file as an argument.")
        sys.exit(1)
    
    # Read solution
    x, y, k, n, boxes, positions, sizes = read_solution(sys.argv[1])
    print(k,x,y)
    print(n,boxes)
    print(positions)
    print(sizes)
    
    # Create visualization
    fig, ax = visualize_grid(x, y, k, boxes, positions, sizes)
    
    # Save the figure
    #plt.savefig('grid_solution.png', dpi=300, bbox_inches='tight')
    
    # Display the figure
    plt.show()

if __name__ == "__main__":
    main()

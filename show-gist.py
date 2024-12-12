"""
Shows solution from Gist.
Reads the file grid.txt.
To launch
python3 show-gist.py <k> <x>
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

def parse_minizinc_array(text):
    """
    Parse a MiniZinc-style array declaration to extract values.
    
    Args:
    text (str): The text containing the array declaration
    
    Returns:
    tuple: (number of boxes, list of positions, list of sizes)
    """
    # Extract number of boxes
    boxes_line = [line for line in text.split('\n') if 'boxes' in line][0]
    boxes = int(boxes_line.split('=')[1].strip().rstrip(';'))
    
    # Extract positions
    positions_line = [line for line in text.split('\n') if 'positions' in line][0]
    positions_str = positions_line.split('[')[1].split(']')[0]
    positions_raw = positions_str.split(', ')
    
    # Convert positions to (x,y) pairs
    positions = []
    for i in range(0, len(positions_raw), 2):
        positions.append((int(positions_raw[i]), int(positions_raw[i+1])))
    
    # Extract sizes
    sizes_line = [line for line in text.split('\n') if 'sizes' in line][0]
    sizes_str = sizes_line.split('[')[1].split(']')[0]
    sizes_raw = sizes_str.split(', ')
    
    # Convert sizes to (width, height) pairs
    sizes = []
    for i in range(0, len(sizes_raw), 2):
        sizes.append((int(sizes_raw[i]), int(sizes_raw[i+1])))
    
    return boxes, positions[:boxes], sizes[:boxes]

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
        
        # Add index text to the box
        # Adjust font size based on box size to ensure visibility
        center_x = pos[0] - 1 + size[0] / 2
        center_y = pos[1] - 1 + size[1] / 2
        fontsize = 20
        ax.text(center_x, center_y, str(idx + 1), 
                ha='center', va='center', 
                fontweight='bold', 
                fontsize=fontsize,
                color='black')
    
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

# Example usage
def main():
    k, x = [int(i) for i in (sys.argv[1:3])]
    y = x + 5

    text = open('grid.txt','r').read()

    #text = b'\n'.join(sys.stdin.readlines())
    # Parse the text
    boxes, positions, sizes = parse_minizinc_array(text)
    print(boxes)
    print(positions)
    print(sizes)

    fig, ax = visualize_grid(x, y, k, boxes, positions, sizes)
    #plt.ion()
    plt.show()


if __name__ == "__main__":
    main()

"""
Shows solution from Gist.
Reads the file grid.txt.
To launch
python3 show-gist.py <k> <x>
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import re

def parse_minizinc_array(text):
    """
    Parse a Gist node to extract values.
    
    Args:
    text (str): The text containing the node content
    
    Returns:
    tuple: (number of boxes, list of positions, list of sizes)
    """

    lines = text.split('\n')
    lines = {line.split(' ')[0]:line for line in lines}

    # Extract number of boxes
    boxes_line = lines['boxes']
    boxes = int(re.findall('[0-9]+',boxes_line)[0])
    
    # Extract positions
    positions_line = lines['positions']
    positions_str = re.findall('\[[0-9, ]+',positions_line)[0] + ']'
    positions_raw = eval(positions_str)
    positions = [(int(positions_raw[i]), int(positions_raw[i+1])) for i in range(0, len(positions_raw), 2)]
    
    # Extract sizes
    sizes_line = lines['sizes']
    sizes_str = re.findall('\[[0-9, ]+',sizes_line)[0] + ']'
    sizes_raw = eval(sizes_str)
    sizes = [(int(sizes_raw[i]), int(sizes_raw[i+1])) for i in range(0, len(sizes_raw), 2)]

    boxes = min(boxes, len(sizes), len(positions))
    
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
    k, x, y = [int(i) for i in (sys.argv[1:4])]

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

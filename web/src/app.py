from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import re

app = Flask(__name__)

def parse_gist(text):
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


def parse_gecode(solution):
    """
    Read and parse the solution file
    """    

    # Parse boxes
    boxes = int(solution.split('***')[3].split('\n')[1].split(' ')[1])
    
    # Parse positions and sizes
    positions = solution.split('***')[1][len('positions:'):].split('\n')[1:-1]
    positions = [(int(pos.split(',')[0]),int(pos.split(',')[1])) for pos in positions[:boxes]]
    
    sizes = solution.split('***')[2][len('sizes:'):].split('\n')[1:-1]
    sizes = [(int(size.split(',')[0]),int(size.split(',')[1])) for size in sizes[:boxes]]
    
    boxes = min(boxes, len(sizes), len(positions))
    
    return boxes, positions[:boxes], sizes[:boxes]

def parse_minizinc(text):
    if '*' in text:
        return parse_gecode(text)
    else:
        return parse_gist(text)

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



@app.route('/', methods=['GET', 'POST'])
def index():
    text_content = ""
    plot_url = None

    if request.method == 'POST':
        text_content = request.form['text_content']
        x_value = request.form.get('x', '')
        y_value = request.form.get('y', '')
        k_value = request.form.get('k', '')

        # Validate and process the inputs
        try:
            x = int(x_value) if x_value else 1
            y = int(y_value) if y_value else 1
            k = int(k_value) if k_value else 1
        except ValueError:
            x, y, k = 1, 1, 1  # Default to 1 if inputs are invalid

        boxes, positions, sizes = parse_minizinc(text_content)

        fig, ax = visualize_grid(x, y, k, boxes, positions, sizes)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plot_url = f"data:image/png;base64,{plot_data}"
        plt.close(fig)  # Close the figure to release memory

    return render_template('index.html', text_content=text_content, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)


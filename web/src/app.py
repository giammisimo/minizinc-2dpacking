from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

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
        ax.text(center_x, center_y, str(idx), 
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

        boxes, positions, sizes = parse_minizinc_array(text_content)

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


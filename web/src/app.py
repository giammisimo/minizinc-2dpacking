from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import re
import hashlib
import os
from pathlib import Path

app = Flask(__name__)

# Create cache directory if it doesn't exist
CACHE_DIR = Path(__file__).parent / 'static' / 'cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_key(text_content):
    """Generate a unique hash key for the input text"""
    return hashlib.md5(text_content.encode('utf-8')).hexdigest()

def get_cached_image(cache_key):
    """Try to get a cached image"""
    cache_file = CACHE_DIR / f"{cache_key}.png"
    if cache_file.exists():
        with open(cache_file, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

def save_to_cache(cache_key, fig):
    """Save the generated plot to cache"""
    cache_file = CACHE_DIR / f"{cache_key}.png"
    plt.savefig(cache_file, format='png', bbox_inches='tight')

def extract_parameters(text):
    """
    Extract x, y, k parameters from the input text
    """
    params = {}
    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':')
            key = key.strip().lower()
            if key in ['x', 'y', 'k']:
                try:
                    params[key] = int(value.strip())
                except ValueError:
                    continue
    return params.get('x', 1), params.get('y', 1), params.get('k', 1)

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
        box_color = colors[idx % len(colors)]
        # Adjust for coordinate system (bottom-left origin)
        ax.add_patch(plt.Rectangle((pos[0]-1, pos[1]-1), 
                                   size[0], size[1], 
                                   facecolor=box_color,
                                   edgecolor='black',
                                   alpha=0.7))
        
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

        if not text_content:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, 'Errore: text_content mancante', fontsize=12, ha='center')
            ax.axis('off')
            
            # Generate error image
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plot_url = f"data:image/png;base64,{plot_data}"
            plt.close(fig)
        else:
            # Check cache first
            cache_key = get_cache_key(text_content)
            cached_image = get_cached_image(cache_key)
            
            if cached_image:
                plot_url = f"data:image/png;base64,{cached_image}"
            else:
                # Generate new image if not in cache
                x, y, k = extract_parameters(text_content)
                boxes, positions, sizes = parse_minizinc(text_content)
                fig, ax = visualize_grid(x, y, k, boxes, positions, sizes)
                
                # Save to cache
                save_to_cache(cache_key, fig)
                
                # Convert to base64 for display
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                buf.close()
                plot_url = f"data:image/png;base64,{plot_data}"
                plt.close(fig)  # Close the figure to release memory

    return render_template('index.html', text_content=text_content, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)


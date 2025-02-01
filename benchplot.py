import sys
import os
import glob
import re
import matplotlib.pyplot as plt

TIME_LIMIT = 300

def extract_params_and_time(text_content):
    """
    Given the text content of a file, extracts:
      - x, y, k (if available)
      - the last time value found in '% time elapsed: ... s'
    Returns (x, y, k, time) or (None, None, None, None) if not found.
    """
    pattern_x = re.compile(r'^x:\s*(\d+)', re.MULTILINE)
    pattern_y = re.compile(r'^y:\s*(\d+)', re.MULTILINE)
    pattern_k = re.compile(r'^k:\s*(\d+)', re.MULTILINE)
    pattern_time = re.compile(r'% time elapsed:\s*([\d.]+)\s*s')

    x_matches = pattern_x.findall(text_content)
    y_matches = pattern_y.findall(text_content)
    k_matches = pattern_k.findall(text_content)
    time_matches = pattern_time.findall(text_content)

    x_val = int(x_matches[0]) if x_matches else None
    y_val = int(y_matches[0]) if y_matches else None
    k_val = int(k_matches[0]) if k_matches else None
    time_val = float(time_matches[-1]) if time_matches else None

    return x_val, y_val, k_val, time_val

def main():
    # Get folder path from command line or default to current directory
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = "."

    results = {}

    # Search for all files matching "bench*.txt" in the specified folder
    search_pattern = os.path.join(folder_path, "bench*.txt")
    for filename in glob.glob(search_pattern):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        unsat = "UNSATISFIABLE" in content
        x_val, y_val, k_val, time_val = extract_params_and_time(content)

        # If the file is unsatisfiable, log it but skip plotting since x,y,k might not exist
        if unsat:
            print(f"[INFO] File {filename} is unsatisfiable (UNSAT).")
        
        # We only plot if x, y, k, time are found
        if x_val is not None and y_val is not None and k_val is not None and time_val is not None and time_val < TIME_LIMIT:
            key = (x_val, y_val)
            if key not in results:
                results[key] = []
            results[key].append((k_val, time_val))
        else:
            print(f"[WARNING] Could not find parameters/time in file: {filename}")

    # Create the plot (k on X-axis, time on Y-axis)
    plt.figure(figsize=(10, 6))

    # Use the new recommended approach to get a colormap
    # (available in Matplotlib 3.7+)
    colormap = plt.colormaps.get_cmap('rainbow')

    sorted_keys = sorted(results.keys())
    num_keys = len(sorted_keys)

    for i, (x_val, y_val) in enumerate(sorted_keys):
        data = results[(x_val, y_val)]
        # Sort data points by k
        data_sorted = sorted(data, key=lambda t: t[0])
        ks = [d[0] for d in data_sorted]
        times = [d[1] for d in data_sorted]
        
        color = colormap(i / num_keys)
        plt.plot(ks, times, marker='o', color=color, label=f"x={x_val}, y={y_val}")

    plt.title("Execution Time as a Function of k")
    plt.xlabel("k")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

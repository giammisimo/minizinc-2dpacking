import tkinter as tk
import re

s = '''
positions = 
[| 1,  1
 | 1, 11
 | 6,  6
 | 6,  1
 |];
sizes = 
[|  5, 10
 | 10,  5
 | 10,  5
 | 10,  5
 |];
'''
s = re.sub('\n','',s)
s = re.sub('\[\| ','[[',s)
s = re.sub(' \|\]',']]',s)
s = re.sub(' \| ','],[',s)
s = re.sub('[a-z]+ = ','',s)
positions, sizes = (*s.split(';')[:-1],)

positions = eval(positions)
sizes = eval(sizes)
print('positions',positions)
print('sizes',sizes)

class GridGUI:
    def __init__(self, grid_size: int, cell_size: int):
        # Creating the root window
        self.root = tk.Tk()
        self.root.title("Grid GUI")

        # Creating the canvas widget
        self.canvas = tk.Canvas(self.root, width=grid_size*cell_size, height=grid_size*cell_size)
        self.canvas.pack()

        # Setting the grid size and cell size
        self.grid_size = grid_size
        self.cell_size = cell_size

        # Dictionary to store the colors for different square sizes
        self.square_colors = {
            1: "yellow",
            2: "red",
            3: "green",
            4: "blue",
            5:"orange",
            6:"purple",
            7: "brown"
        }

    def draw_grid(self):
        """
        Draws the grid on the canvas.
        """

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def place_box(self, index: int, sizex: int, sizey: int, row: int, col: int):
        color = self.square_colors[index]

        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + sizex * self.cell_size
        y2 = y1 + sizey * self.cell_size

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def run(self):
        self.root.mainloop()

## Gridsize(k, cellSize)
gui = GridGUI(19, 20)
gui.draw_grid()

for i in range(len(sizes)):
    gui.place_box(i+1,sizes[i][1],sizes[i][0],positions[i][0]-1,positions[i][1]-1)

gui.run()
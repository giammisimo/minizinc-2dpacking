import tkinter as tk
import sys

solution = open(sys.argv[1],'r').read()

parameters = solution.split('***')[0].split('\n')[:-1]
x, y, k, n = tuple([int(par.split(' ')[1]) for par in parameters])
print('x',x)
print('y',y)
print('k',k)
print('n',n)

boxes = int(solution.split('***')[3].split('\n')[1].split(' ')[1])
print('boxes',boxes)

positions = solution.split('***')[1][len('positions:'):].split('\n')[1:-1]
positions = [(int(pos.split(',')[0]),int(pos.split(',')[1])) for pos in positions[:boxes]]

sizes = solution.split('***')[2][len('sizes:'):].split('\n')[1:-1]
sizes = [(int(size.split(',')[0]),int(size.split(',')[1])) for size in sizes[:boxes]]

print('positions',positions)
print('sizes',sizes)

# old parsing for the default minzinc formatting
# positions = 
# [| 1,  1
#  | 1, 11
#  | 6,  6
#  | 6,  1
#  |];
# sizes = 
# [|  5, 10
#  | 10,  5
#  | 10,  5
#  | 10,  5
#  |];
# s = re.sub('\n','',s)
# s = re.sub('\[\| ','[[',s)
# s = re.sub(' \|\]',']]',s)
# s = re.sub(' \| ','],[',s)
# s = re.sub('[a-z]+ = ','',s)
# positions, sizes = (*s.split(';')[:-1],)
# positions = eval(positions)
# sizes = eval(sizes)

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
gui = GridGUI(k, 30)
gui.draw_grid()

for i in range(boxes):
    gui.place_box(i+1,sizes[i][1],sizes[i][0],positions[i][0]-1,positions[i][1]-1)

gui.run()
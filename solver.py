import numpy as np
from PIL import Image
import Node

def conv(var):
    if var:
        return 1
    return 0

image = Image.open('maze2.png')
i = np.array(image)
convert = image.convert('1')
img = np.array(convert)
maze = []
for row in img:
    maze.append(list(map(lambda x: conv(x), row)))

print("maze len:",int(len(maze)) > 3)
def can_move_vertical(row, col):
    if (int(len(maze)) > row and maze[row+1][col] == 1) or (row > 0 and maze[row-1][col] == 1):
        return True
    return False
def can_move_horizontal(row_, row):
    if (row < len(row_) - 1 and row_[col - 1] == 1) or row > 0 and row_[col + 1] == 1:
        return True
    return False
nodes = []
for row in range(len(maze)):
    row_ = maze[row]
    for col in range(len(row_)):
        if row_[col] == 1:
            if can_move_vertical(row, col):
                if row == 0 or row == len(maze)-1:
                    nodes.append(Node.Node(row, col, True))
                if can_move_horizontal(row_, row):
                    nodes.append(Node.Node(row, col))
            if can_move_horizontal(row_, row):
                if col == 0 or col == len(row_)-1:
                    nodes.append(Node.Node(row, col, True))

#
for n in nodes:
    print(str(n))
    i[n.get_row()][n.get_col()] = 125;

fromarray = Image.fromarray(i)
fromarray.save("dupa.png")
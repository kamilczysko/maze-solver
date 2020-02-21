import numpy as np
from PIL import Image
import Node
import sys

sys.setrecursionlimit(100000000)


def conv(var):
    if var:
        return 1
    return 0


image = Image.open('maze_massive.png')
i = np.array(image)
convert = image.convert('1')
img = np.array(convert)
maze = []
for row_num in img:
    maze.append(list(map(lambda x: conv(x), row_num)))


def can_move_vertical(row_num, col_num):
    if (len(maze) - 1 > row_num and maze[row_num + 1][col_num] == 1) or (
            row_num > 0 and maze[row_num - 1][col_num] == 1):
        return True
    return False


def can_move_horizontal(row_num, col_num):
    if (col_num < len(maze[row_num]) and maze[row_num][col_num + 1] == 1) or (
            col_num > 0 and maze[row_num][col_num - 1] == 1):
        return True
    return False


nodes = []


def find_entry(maze_array):
    first_row = maze_array[0]
    for c in range(len(first_row)):  # check entry in first row
        if (first_row[c] == 1):
            return Node.Node(0, c, True)
    for r in range(len(maze_array)):  # check entry on left wall
        if maze_array[r][0] == 1:
            return Node.Node(r, 0, True)

    for r in range(len(maze_array)):  # check entry on right wall
        if maze_array[r][-1] == 1:
            return Node.Node(r, len(first_row) - 1, True)
    last_row = maze_array[-1]
    for c in range(len(last_row)):  # check entry in first row
        if (first_row[c] == 1):
            return Node.Node(len(maze_array) - 1, c, True)

    return None


def if_start_or_exit(row, col):
    if row == 0 or col == 0:
        return True
    if row == len(maze) - 1 or col == len(maze[0]) - 1:
        return True
    return False


def get_node_on_right(node):
    if node.col < len(maze[node.row]) - 1:
        i = node.col
        i += 1
        while i <= (len(maze[node.row]) - 1) and maze[node.row][i] == 1:
            if can_move_vertical(node.row, i) or if_start_or_exit(node.row, i):
                new_node = Node.Node(node.row, i, i == len(maze[node.row]) - 1)
                # node.add_child(new_node)
                return new_node
            i += 1
        return None


def get_node_on_left(node):
    if node.col > 0:
        i = node.col
        i -= 1
        while i >= 0 and maze[node.row][i] == 1:
            if can_move_vertical(node.row, i) or if_start_or_exit(node.row, i):
                new_node = Node.Node(node.row, i, i == 0)
                # node.add_child(new_node)
                return new_node
            i -= 1
        return None


def get_node_on_top(node):
    if node.row > 0:
        i = node.row
        i -= 1
        while i >= 0 and maze[i][node.col] == 1:
            if can_move_horizontal(i, node.col) or if_start_or_exit(i, node.col):
                new_node = Node.Node(i, node.col, i == 0)
                # node.add_child(new_node)
                return new_node
            i -= 1
        return None


def get_node_on_down(node):
    if node.row < len(maze) - 1:
        i = node.row
        i += 1
        while i <= (len(maze) - 1) and maze[i][node.col] == 1:
            if can_move_horizontal(i, node.col) or if_start_or_exit(i, node.col):
                new_node = Node.Node(i, node.col, i == len(maze) - 1)
                # node.add_child(new_node)
                return new_node
            i += 1
        return None


def set_green(row, col):
    i[row][col][0] = 0;
    i[row][col][1] = 250;
    i[row][col][2] = 0;


def set_blue(row, col):
    i[row][col][0] = 0;
    i[row][col][1] = 0;
    i[row][col][2] = 250;
    i[row][col][3] = 250;


result_path = []
entry = find_entry(maze)
result_path.append(entry)

top = get_node_on_top(entry)
left = get_node_on_left(entry)
down = get_node_on_down(entry)
right = get_node_on_right(entry)
second_node = list(filter(None, [top, down, left, right]))
if len(second_node) > 1:
    print("do dupy labirynt, wejście kajś w dupie")
    exit(0)
next_node = second_node[0]
entry.add_child(next_node)

result_path.append(next_node)
set_blue(entry.row, entry.col)
set_blue(next_node.row, next_node.col)


def find_next_node(node, prev_node):
    top = get_node_on_top(node)
    left = get_node_on_left(node)
    down = get_node_on_down(node)
    right = get_node_on_right(node)
    nds = [top, down, left, right]
    if prev_node in nds:
        nds.remove(prev_node)
    next_move = list(filter(None, nds))
    for move in next_move:
        if move.entry == False:
            if find_next_node(move, node):
                set_blue(move.row, move.col)
                result_path.append(move)
                node.add_child(move)
                return True
        else:
            result_path.append(move)
            set_blue(move.row, move.col)
            node.add_child(move)
            return True


find_next_node(next_node, entry)


def get_iter_params(a, b):
    step = -1
    if a - b < 0:
        step = 1
    return step


def get_route(start, end):
    if start.get_row() == end.get_row():
        step = get_iter_params(start.get_col(), end.get_col())
        for c in range(start.get_col(), end.get_col(), step):
            set_blue(start.get_row(), c)
    elif start.get_col() == end.get_col():
        step = get_iter_params(start.get_row(), end.get_row())
        for c in range(start.get_row(), end.get_row(), step):
            set_blue(c, start.get_col())


f_node = result_path[0]


def draw_path(node):
    child = node.get_next_child()
    if child is None:
        return
    get_route(node, child)
    draw_path(child)


draw_path(f_node)

fromarray = Image.fromarray(i)
fromarray.save("dupa2.png")

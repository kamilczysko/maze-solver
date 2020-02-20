import numpy as np
from PIL import Image
import Node


def conv(var):
    if var:
        return 1
    return 0


image = Image.open('maze_big.png')
i = np.array(image)
convert = image.convert('1')
img = np.array(convert)
maze = []
for row_num in img:
    maze.append(list(map(lambda x: conv(x), row_num)))


def can_move_vertical(row_num, col_num):
    if (len(maze) > row_num and maze[row_num + 1][col_num] == 1) or (row_num > 0 and maze[row_num - 1][col_num] == 1):
        return True
    return False


def can_move_horizontal(row_num, col_num):
    if (col_num < len(maze[row_num]) and maze[row_num][col_num + 1] == 1) or (
            col_num > 0 and maze[row_num][col_num - 1] == 1):
        return True
    return False


nodes = []
for row_num in range(len(maze)):
    row = maze[row_num]
    for col_num in range(len(row)):
        if row[col_num] == 1:
            if can_move_vertical(row_num, col_num):
                if row_num == 0 or row_num == len(maze) - 1:
                    nodes.append(Node.Node(row_num, col_num, True))
                if can_move_horizontal(row_num, col_num):
                    nodes.append(Node.Node(row_num, col_num))
            if can_move_horizontal(row_num, row_num):
                if col_num == 0 or col_num == len(row) - 1:
                    nodes.append(Node.Node(row_num, col_num, True))

for n in nodes:
    # print(str(n))
    i[n.get_row()][n.get_col()][0] = 250;
    i[n.get_row()][n.get_col()][1] = 0;
    i[n.get_row()][n.get_col()][2] = 0;


def get_node(row, col):
    for n in nodes:
        if n.is_in_location(row, col):
            return n
    return None


def get_node_on_right(row, col):
    if col < len(maze[row]) - 1:
        i = col
        i += 1
        while maze[row][i] == 1 and col < len(maze[row]) - 1:
            node = get_node(row, i)
            if node is not None:
                return node
            i += 1
        return None


def get_node_on_left(row, col):
    if col > 0:
        i = col
        i -= 1
        while maze[row][i] == 1 and col > 0:
            node = get_node(row, i)
            if node is not None:
                return node
            i -= 1
        return None


def get_node_on_top(row, col):
    if row > 0:
        i = row
        i -= 1
        while maze[i][col] == 1 and i > 0:
            node = get_node(i, col)
            if node is not None:
                return node
            i -= 1
        return None

def get_node_on_down(row_num, col):
    i = row_num
    if row_num < len(maze) - 1:
        i += 1
        while maze[i][col] == 1 and i < len(maze) - 1:
            node = get_node(i, col)
            if node is not None:
                return node
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

def reduce_nodes():
    is_free = True
    print("reduce: ", len(nodes))
    for n in nodes:
        row_num = int(n.row)
        col_num = int(n.col)
        top = get_node_on_top(row_num, col_num)
        down = get_node_on_down(row_num, col_num)
        left = get_node_on_left(row_num, col_num)
        right = get_node_on_right(row_num, col_num)
        lst = [top, down, left, right]
        if lst.count(None) == 3:
            if not n.is_entry():
                set_green(row_num, col_num)
                nodes.remove(n)
                is_free = False
    if not is_free:
        reduce_nodes()
    return is_free


print(len(nodes), " - nodes")
reduce_nodes()
print(len(nodes), " - nodes")

def get_start_node():
    for n in nodes:
        if n.is_entry():
            return n
    return None

def get_iter_params(a,b):
    step = -1
    if a-b < 0:
        step = 1
    return step

def get_route(start, end):
    path=[]
    if start.get_row() == end.get_row():
        step = get_iter_params(start.get_col(), end.get_col())
        for c in range(start.get_col(), end.get_col(), step):
            path.append(Node.Node(start.get_row(), c))
    elif start.get_col() == end.get_col():
        step = get_iter_params(start.get_row(), end.get_row())
        for c in range(start.get_row(), end.get_row(), step):
            path.append(Node.Node(c, start.get_col()))
    path.append(end)
    return path

walk_result = []
start_node = get_start_node()
walk_result.append(start_node)
if start_node is not None:
    is_end = False
    actual_node = start_node
    while (not is_end):
        row_num = actual_node.row
        col_num = actual_node.col
        top = get_node_on_top(row_num, col_num)
        down = get_node_on_down(row_num, col_num)
        left = get_node_on_left(row_num, col_num)
        right = get_node_on_right(row_num, col_num)
        n = list(filter(None ,[top, down, left, right]))
        tmp_path = []
        if n[0] not in walk_result:
            tmp_path = get_route(walk_result[-1], n[0])
        if len(n) > 1 and n[1] not in walk_result:
            tmp_path = get_route(walk_result[-1], n[1])
        walk_result.extend(tmp_path)
        if walk_result[-1].is_entry():
            is_end = True
        actual_node = walk_result[-1]

for n in walk_result:
    set_blue(n.get_row(), n.get_col())

fromarray = Image.fromarray(i)
fromarray.save("dupa.png")

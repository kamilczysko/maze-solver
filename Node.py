class Node:

    def __init__(self, row, col, entry=False):
        self.row = row
        self.col = col
        self.children = []
        self.children_iterator = iter(self.children)
        self.entry = entry

    def is_entry(self):
        return self.entry

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def is_in_location(self, row, col):
        return self.row == row and self.col == col

    def get_number_of_children(self):
        return len(self.children)

    def get_next_child(self):
        try:
            return next(self.children_iterator)
        except:
            return None

    def __eq__(self, o) -> bool:
        if o is None:
            return False
        return self.row == o.row and self.col == o.col

    def is_in_location(self, x, y):
        return self.row == x and self.col == y

    def add_child(self, child):
        self.children.append(child)

    def has_child(self, child):
        return child in self.children

    def __str__(self):
        return str(self.row) + " - " + str(self.col) + " - " + str(self.children) + " - " + str(self.entry)


import Node

n1 = Node.Node(1, 2)
n2 = Node.Node(2, 2)
n3 = Node.Node(1, 2)

l = [n1,n2]

print(l)

l.remove(n3)

print(l)
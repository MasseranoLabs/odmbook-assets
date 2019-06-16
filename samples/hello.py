from pyodm import Node, exceptions

node = Node('localhost', 3000)
try:
    print(node.info())
except exceptions.NodeConnectionError as e:
    print("Cannot connect: " + str(e))
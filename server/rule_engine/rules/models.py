# models.py

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

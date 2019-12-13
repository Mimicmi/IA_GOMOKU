from copy import copy

class Node:
    def __init__(self, data, size):
        self.data = data
        self.next = []
        self.size = size
        self.eval = None
        self.playedCase = None
    
    def append(self, node):
        self.next.append(node)

    def addChild(self, case, value):
        child = Node(None, self.size)
        child.data = self.data[:]
        child.data[case.ligne][case.colonne] = value
        self.next.append(child)

    def display(self):
        self.printNode()

    def printNode(self):
        for ligne in range(self.size):
            for colonne in range(self.size):
                print(self.data[ligne][colonne], " ", end='')
            print('')
        print('')
        print('')

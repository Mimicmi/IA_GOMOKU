import os
import platform
from copy import copy

target = 3
class Board:
    def __init__(self, size):
        self.size = size
        self.tab = [['.'] * size for i in range(size)]
       
    def reinit(self):
        self.tab = [['.'] * self.size for i in range(self.size)]
        
    def display(self):
        # if platform.system() == "Windows":
        #     os.system("cls")
        # elif platform.system() == "Linux" or platform.system() == "Darwin":
        #     os.system("clear")

        print("   ", end='')
        for i in range(self.size):
            print(i, " ", end='')
        print('')

        for ligne in range(self.size):
            print(ligne, " ", end='')
            for colonne in range(self.size):
                print(self.tab[ligne][colonne], " ", end='')
            print('')
    
    def turn(self, case):
        self.tab[case.ligne][case.colonne] = 2

    def board(self, case, value):
        self.tab[case.ligne][case.colonne] = value

    def countRowCol(self, case, direction):
        _copy = copy(case)
        n = 0
        value = self.tab[_copy.ligne][_copy.colonne]

        while (_copy.colonne + 1 < self.size and self.tab[_copy.ligne][_copy.colonne+1] == value):
            if direction == "row":
                _copy.colonne += 1
            elif direction == "col":
                _copy.ligne += 1
        
        while (_copy.colonne >= 0 and self.tab[_copy.ligne][_copy.colonne] == value):
            n+=1
            if direction == "row":
                _copy.colonne -= 1
            elif direction == "col":
                _copy.ligne -= 1

        return n

    def countDecreaseDiagonal(self, case):
        _copy = copy(case)
        n = 0
        value = self.tab[_copy.ligne][_copy.colonne]

        while _copy.ligne + 1 < self.size and _copy.colonne + 1 < self.size and self.tab[_copy.ligne+1][_copy.colonne + 1] == value:
            _copy.ligne += 1
            _copy.colonne += 1
        
        while _copy.ligne >= 0 and _copy.colonne >= 0 and self.tab[_copy.ligne][_copy.colonne] == value:
            n+=1
            _copy.ligne -= 1
            _copy.colonne -=1

        return n

    def countIncreaseDiagonal(self, case):
        _copy = copy(case)
        n = 0
        value = self.tab[_copy.ligne][_copy.colonne]

        while _copy.ligne - 1 > 0 and _copy.colonne + 1 < self.size and self.tab[_copy.ligne - 1][_copy.colonne + 1] == value:
            _copy.ligne -= 1
            _copy.colonne += 1
        
        while (_copy.ligne < self.size and _copy.colonne > 0 and self.tab[_copy.ligne][_copy.colonne] == value):
            n+=1
            _copy.ligne += 1
            _copy.colonne -=1

        return n
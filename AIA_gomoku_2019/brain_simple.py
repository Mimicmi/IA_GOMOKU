import random
from case import Case
from copy import copy

class Brain_simple:
    def __init__(self, board):
        self.board = board
        self.size = self.board.size
        self.cord = Case(0,0)

        self.endRow = None
        self.startRow = None

        self.endCol = None
        self.startCol = None

        self.endDecDiag = None
        self.startDecDiag = None

        self.endIncDiag = None
        self.startIncDiag = None

    def countRow(self, turncord):
        n = 0
        _turncord = copy(turncord)
        value = self.board.tab[_turncord.ligne][_turncord.colonne]

        while (_turncord.colonne + 1 < self.size and self.board.tab[_turncord.ligne][_turncord.colonne + 1] == value):
            _turncord.colonne += 1

        self.endRow = Case(_turncord.ligne, _turncord.colonne)

        while (_turncord.colonne >= 0 and self.board.tab[_turncord.ligne][_turncord.colonne] == value):
            n += 1
            _turncord.colonne -= 1

        self.startRow = Case(_turncord.ligne, _turncord.colonne)

        return n >= 2
    
    def countCol(self, turncord):
        n = 0
        _turncord = copy(turncord)
        value = self.board.tab[_turncord.ligne][_turncord.colonne]

        while (_turncord.ligne + 1 < self.size and self.board.tab[_turncord.ligne + 1][_turncord.colonne] == value):
            _turncord.ligne += 1

        self.endCol = Case(_turncord.ligne, _turncord.colonne)

        while (_turncord.ligne >= 0 and self.board.tab[_turncord.ligne][_turncord.colonne] == value):
            n += 1
            _turncord.ligne -= 1

        self.startCol = Case(_turncord.ligne, _turncord.colonne)

        return n >= 2
    
    def countIncDiagonal(self, case):
        _copy = copy(case)
        n = 0
        value = self.board.tab[_copy.ligne][_copy.colonne]

        while _copy.ligne + 1 < self.size and _copy.colonne + 1 < self.size and self.board.tab[_copy.ligne+1][_copy.colonne + 1] == value:
            _copy.ligne += 1
            _copy.colonne += 1

        self.endIncDiag = Case(_copy.ligne, _copy.colonne)

        while _copy.ligne >= 0 and _copy.colonne >= 0 and self.board.tab[_copy.ligne][_copy.colonne] == value:
            n+=1
            _copy.ligne -= 1
            _copy.colonne -=1

        self.startIncDiag = Case(_copy.ligne, _copy.colonne)

        return n >= 2

    def countDecDiagonal(self, case):
        _copy = copy(case)
        n = 0
        value = self.board.tab[_copy.ligne][_copy.colonne]

        while _copy.ligne - 1 > 0 and _copy.colonne + 1 < self.size and self.board.tab[_copy.ligne - 1][_copy.colonne + 1] == value:
            _copy.ligne -= 1
            _copy.colonne += 1

        self.endDecDiag = Case(_copy.ligne, _copy.colonne)
        
        while (_copy.ligne < self.size and _copy.colonne > 0 and self.board.tab[_copy.ligne][_copy.colonne] == value):
            n+=1
            _copy.ligne += 1
            _copy.colonne -=1

        self.startDecDiag = Case(_copy.ligne, _copy.colonne)

        return n >= 2
    
    def getRandomCase(self):
        case = Case(random.randint(0, self.board.size-1), random.randint(0, self.board.size-1))
        while (self.board.tab[case.ligne][case.colonne] != "."):
            case = Case(random.randint(0, self.board.size-1), random.randint(0, self.board.size-1))
        
        return case
    
    def playRandom(self):
        case = self.getRandomCase()
        return case

    def playSafe(self, opponnentMove, numTurn):
        if numTurn == 1:
            self.cord = self.playRandom()
        elif self.countCol(opponnentMove):
            if self.startCol.ligne >= 0 and self.startCol.colonne >= 0 and self.board.tab[self.startCol.ligne][self.startCol.colonne] == '.':
                self.cord = Case(self.startCol.ligne, self.startCol.colonne)

            elif self.endCol.ligne + 1 < self.size and self.board.tab[self.endCol.ligne + 1][self.endCol.colonne] == '.':
                self.cord = Case(self.endCol.ligne + 1, self.endCol.colonne)

        elif self.countRow(opponnentMove):
            if self.startRow.ligne >= 0 and self.startRow.colonne >= 0 and self.board.tab[self.startRow.ligne][self.startRow.colonne] == '.':
                self.cord = Case(self.startRow.ligne, self.startRow.colonne)

            elif self.endRow.colonne + 1 < self.size and self.board.tab[self.endRow.ligne][self.endRow.colonne + 1] == '.':
                self.cord = Case(self.endRow.ligne, self.endRow.colonne + 1)

        elif self.countIncDiagonal(opponnentMove):
            if self.startIncDiag.ligne >= 0 and self.startIncDiag.colonne >= 0 and self.board.tab[self.startIncDiag.ligne][self.startIncDiag.colonne] == '.':
                self.cord = Case(self.startIncDiag.ligne, self.startIncDiag.colonne)

            elif self.endIncDiag.ligne + 1 < self.size and self.endIncDiag.colonne + 1 < self.size and self.board.tab[self.endIncDiag.ligne + 1][self.endIncDiag.colonne + 1] == '.':
                self.cord = Case(self.endIncDiag.ligne + 1, self.endIncDiag.colonne + 1)  

        elif self.countDecDiagonal(opponnentMove):
            if self.startDecDiag.ligne >= 0 and self.startDecDiag.colonne >= 0 and self.board.tab[self.startDecDiag.ligne][self.startDecDiag.colonne] == '.':
                self.cord = Case(self.startDecDiag.ligne, self.startDecDiag.colonne)

            elif self.endDecDiag.ligne - 1 >= 0 and self.endDecDiag.colonne + 1 < self.size and self.board.tab[self.endDecDiag.ligne - 1][self.endDecDiag.colonne + 1] == '.':
                self.cord = Case(self.endDecDiag.ligne - 1, self.endDecDiag.colonne + 1)

        else:
            self.cord = self.playAgro(numTurn)

        self.board.tab[self.cord.ligne][self.cord.colonne] = 1
        print(self.cord.ligne, ',', self.cord.colonne, sep='', flush=True)
        return self.cord
    
    def playAgro(self, numTurn):
        if self.countCol(self.cord) == False and self.countRow(self.cord) == False and self.countDecDiagonal(self.cord) == False and self.countIncDiagonal(self.cord) == False:
            self.cord.ligne = random.randint(0, self.size - 1)
            self.cord.colonne = random.randint(0, self.size - 1)
            while (self.board.tab[self.cord.ligne][self.cord.colonne] != "."):
                self.cord.ligne = random.randint(0, self.size - 1)
                self.cord.colonne = random.randint(0, self.size - 1)

        elif self.countCol(self.cord):
            if self.startCol.ligne >= 0 and self.startCol.colonne >= 0 and self.board.tab[self.startCol.ligne][self.startCol.colonne] == '.':
                self.cord = Case(self.startCol.ligne, self.startCol.colonne)

            elif self.endCol.ligne + 1 < self.size and self.board.tab[self.endCol.ligne + 1][self.endCol.colonne] == '.':
                self.cord = Case(self.endCol.ligne + 1, self.endCol.colonne)

        elif self.countRow(self.cord):
            if self.startRow.ligne >= 0 and self.startRow.colonne >= 0 and self.board.tab[self.startRow.ligne][self.startRow.colonne] == '.':
                self.cord = Case(self.startRow.ligne, self.startRow.colonne)

            elif self.endRow.colonne + 1 < self.size and self.board.tab[self.endRow.ligne][self.endRow.colonne + 1] == '.':
                self.cord = Case(self.endRow.ligne, self.endRow.colonne + 1)

        elif self.countIncDiagonal(self.cord):
            if self.startIncDiag.ligne >= 0 and self.startIncDiag.colonne >= 0 and self.board.tab[self.startIncDiag.ligne][self.startIncDiag.colonne] == '.':
                self.cord = Case(self.startIncDiag.ligne, self.startIncDiag.colonne)

            elif self.endIncDiag.ligne + 1 < self.size and self.endIncDiag.colonne + 1 < self.size and self.board.tab[self.endIncDiag.ligne + 1][self.endIncDiag.colonne + 1] == '.':
                self.cord = Case(self.endIncDiag.ligne + 1, self.endIncDiag.colonne + 1)  

        elif self.countDecDiagonal(self.cord):
            if self.startDecDiag.ligne >= 0 and self.startDecDiag.colonne >= 0 and self.board.tab[self.startDecDiag.ligne][self.startDecDiag.colonne] == '.':
                self.cord = Case(self.startDecDiag.ligne, self.startDecDiag.colonne)

            elif self.endDecDiag.ligne - 1 >= 0 and self.endDecDiag.colonne + 1 < self.size and self.board.tab[self.endDecDiag.ligne - 1][self.endDecDiag.colonne + 1] == '.':
                self.cord = Case(self.endDecDiag.ligne - 1, self.endDecDiag.colonne + 1)

            else:
                self.playRandom()

        return self.cord
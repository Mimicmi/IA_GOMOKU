import random
from case import *
from copy import copy, deepcopy
from node import *
from time import time

# TODO:
# 1. Construire l'arbre
# 2. Fonction eval
# 3. Min max
class Brain:
    def __init__(self, board):
        self.board = board
        self.botName = "Pivil bot"
        self.version = "0.1"
        self.author = "Pivil"
        self.country = "FR"
        self.timeout_turn = 5000
        self.timeout_match = 200000
        self.max_memory = 71680
        self.time_left = 200000
        self.game_type = 0
        self.rule = 1
        self.folder = "."
        self.coordinateMouseX = 0
        self.coordinateMouseY = 0
        self.value = 1   
    
    def getCaseValue(self, case):
        return self.board.tab[case.ligne][case.colonne] 
    
    # def eval_mouse(self):
    #     if self.board.tab[self.coordinateMouseX][self.coordinateMouseY] == '.':
    #         print("No chip here", flush=True)
    #     elif self.board.tab[self.coordinateMouseX][self.coordinateMouseY] == 1:
    #         print("Opponent chip here")
    #     elif self.board.tab[self.coordinateMouseX][self.coordinateMouseY] == 2:
    #         print("Your chip here")

    def play(self):
        case = Case(random.randint(0, self.board.size-1), random.randint(0, self.board.size-1))
        while (self.board.tab[case.ligne][case.colonne] != "."):
            case = Case(random.randint(0, self.board.size-1), random.randint(0, self.board.size-1))
        self.board.tab[case.ligne][case.colonne] = '1'
        print(case.ligne, ",", case.colonne, sep="")
        return case
    
    def about(self):
        print("name:", self.botName, ",", "version:", self.version, ",", "author:", self.author, ",", "country:", self.country, flush=True)
 
    def check3ThreatRow(self, case, player):
        _copy = copy(case)
        row = 0

        # Go to the right until '.' or size limit
        while (_copy.colonne + 1 < self.board.size and self.getCaseValue(_copy) == player):
            _copy.colonne += 1
        
        # Got a '.'
        if self.getCaseValue(_copy) == '.':
            _copy.colonne -= 1
            # Go to the left until '.' or size limit and increment row counter
            while (_copy.colonne -1 > 0 and self.getCaseValue(_copy) == player):
                _copy.colonne -= 1
                row += 1
            if self.getCaseValue(_copy) == '.':
                return row >= 3

        # Got serie of 1 without a '.' 
        else: 
            return False

    def check3ThreatCol(self, case, player):
        _copy = copy(case)
        col = 0

        # Go to the bot until '.', other player value or size limit
        while (_copy.ligne + 1 < self.board.size and self.getCaseValue(_copy) == player):
            _copy.ligne += 1
        
        # Got a '.'
        if self.getCaseValue(_copy) == '.':
            _copy.ligne -= 1
            # Go to the top until '.' or size limit and increment row counter
            while (_copy.ligne -1 > 0 and self.getCaseValue(_copy) == player):
                _copy.ligne -= 1
                col += 1
            if self.getCaseValue(_copy) == '.':
                return col >= 3

        # Got serie of 1 without a '.' 
        else: 
            return False
    
    def check3ThreatIncDiag(self, case, player):
        n = 0
        _copy = copy(case)

        while _copy.ligne - 1 > 0 and _copy.colonne + 1 < self.board.size and self.getCaseValue(_copy) == player:
            _copy.ligne -= 1
            _copy.colonne += 1
        if self.getCaseValue(_copy) == '.':
            _copy.ligne += 1
            _copy.colonne -= 1
            while (_copy.ligne < self.board.size and _copy.colonne > 0 and self.getCaseValue(_copy) == player):
                n+=1
                _copy.ligne += 1
                _copy.colonne -=1

        return n >= 3

    def check3ThreatDecDiag(self, case, player):
        n = 0
        _copy = copy(case)

        while _copy.ligne + 1 < self.board.size and _copy.colonne + 1 < self.board.size and self.getCaseValue(_copy) == player:
            _copy.ligne += 1
            _copy.colonne += 1
        
        if self.getCaseValue(_copy) == '.':
            _copy.ligne -= 1
            _copy.colonne -= 1
            while _copy.ligne >= 0 and _copy.colonne >= 0 and self.getCaseValue(_copy) == player:
                n+=1
                _copy.ligne -= 1
                _copy.colonne -=1

        return n >= 3

    def is3Threat(self, case, player):
        return self.check3ThreatRow(case, player) or self.check3ThreatCol(case, player) or self.check3ThreatIncDiag(case, player) or self.check3ThreatDecDiag(case, player)

    def staticEval(self, node, maximizingPlayer):
        note = 0

        note = max(self.countRowCol(node, 1), self.countDiag(node), self.check3Threat_opti(node))
        if maximizingPlayer == True:
            return note
        else:
            return note * -1

    def check3Threat_opti(self, node):
        patterns6 = []
        patterns7 = []
        patterns5 = ['.',1,1,1,'.'] # C

        patterns6.append(['.',1,1,1,1,2]) # A 1
        patterns6.append([2,1,1,1,1,'.']) # A 2
        patterns6.append(['.',1,1,1,1,'.']) # B
        patterns6.append(['.',1,'.',1,1,'.']) # E 1
        patterns6.append(['.',1,1,'.',1,'.']) # E 2

        patterns7.append([2,'.',1,1,1,'.','.']) # D 1
        patterns7.append(['.','.',1,1,1,'.',2]) # D 2
        
        for ligne in range(node.size - 7):
            for colonne in range(node.size - 7):
                case = Case(ligne, colonne)
                _tmp = []
                _tmp.append(self.getRow(node, case, 7))
                _tmp.append(self.getCol(node, case, 7))
                _tmp.append(self.getDecrDiag(node, case, 7))

                if any(elem in _tmp  for elem in patterns7):
                    return 9000

        for ligne in range(node.size - 6):
            for colonne in range(node.size - 6):
                case = Case(ligne, colonne)
                _tmp = []
                _tmp.append(self.getRow(node, case, 6))
                _tmp.append(self.getCol(node, case, 6))
                _tmp.append(self.getDecrDiag(node, case, 6))

                if any(elem in _tmp  for elem in patterns6):
                    return 9000

        for ligne in range(node.size - 5):
            for colonne in range(node.size - 5):
                case = Case(ligne, colonne)
                _tmp = []
                _tmp.append(self.getRow(node, case, 5))
                _tmp.append(self.getCol(node, case, 5))
                _tmp.append(self.getDecrDiag(node, case, 5))

                if _tmp[0] == patterns5 or _tmp[1] == patterns5 or _tmp[2] == patterns5:
                    return 9000


        return 0
                
    def getRow(self, node, depart, taille):
        return node.data[depart.ligne][depart.colonne: depart.colonne+taille]  

    def getCol(self, node, depart, taille):
        lst = []
        for i in range(taille):
            lst.append(node.data[depart.ligne + i][depart.colonne])
        
        return lst

    def getDecrDiag(self, node, depart, taille):
        lst = []
        for i in range(taille):
            lst.append(node.data[depart.ligne + i][depart.colonne + i])

        return lst
    
    def getIncrDiag(self, node, depart, taille):
        lst = []
        for i in range(taille):
            lst.append(node.data[depart.ligne + i][depart.colonne - i])

        return lst

    def countRowCol(self, node, player):
        notes = []

        for ligne in range(node.size):
            for colonne in range(node.size):
                value = node.data[ligne][colonne]
                if value == player:
                    note = 1
                    while colonne + 1 < node.size and node.data[ligne][colonne + 1] == value:
                        note += 1
                        colonne += 1

                    notes.append(note)

        for ligne in range(node.size):
            for colonne in range(node.size):
                value = node.data[ligne][colonne]
                if value == player:
                    note = 1
                    while ligne + 1 < node.size and node.data[ligne + 1][colonne] == value:
                        note += 1
                        colonne += 1

                    notes.append(note)

        maxNote = 0

        for n in notes:
            maxNote = max(maxNote, n)

        return maxNote
    
    def countDiag(self, node):
        notes = []

        for ligne in range(node.size):
            for colonne in range(node.size):
                value = node.data[ligne][colonne]
                if value == 1:
                    note = 1
                    while ligne + 1 < node.size and colonne - 1 >= 0 and node.data[ligne + 1][colonne - 1] == value:
                        note += 1
                        colonne += 1
                        ligne -= 1

                    notes.append(note)

        for ligne in range(node.size):
            for colonne in range(node.size):
                value = node.data[ligne][colonne]
                if value == 1:
                    note = 1
                    while ligne + 1 < node.size and colonne + 1 < node.size and node.data[ligne + 1][colonne + 1] == value:
                        note += 1
                        colonne += 1
                        ligne += 1

                    notes.append(note)

        maxNote = 0

        for n in notes:
            maxNote = max(maxNote, n)

        return maxNote

    def minmax(self, node, depth, maximizingPlayer):
        if depth == 0:
            return self.staticEval(node, maximizingPlayer)

        if maximizingPlayer:
            player = 2
        else:
            player = 1
        
        self.createNode(node, player)

        if maximizingPlayer:
            maxEval = -9999
            for i in node.next:
                eval = self.minmax(i, depth - 1, False)
                maxEval = max(maxEval, eval)
            node.eval = maxEval
            return maxEval

        else:
            minEval = 9999
            for i in node.next:
                eval = self.minmax(i, depth - 1, True)
                minEval = min(minEval, eval)
            node.eval = minEval
            return minEval

<<<<<<< HEAD
    def createNode(self, node, value):
        for ligne in range(node.size):
            for colonne in range (node.size):
                if node.data[ligne][colonne] == '.':
                    n = Node(node.data, node.size)
                    n.data[ligne][colonne] = value
                    n.playedCase = Case(ligne, colonne)
                    node.next.append(n)

    def test(self):
        tab = [['.'] * 3 for i in range(3)]
        root = Node(tab, 3)
        self.createNode(root, 2)
        for node in root.next:
            node.printNode()
=======
    def createNode(self, parent, value):
        # lecture tableau
        # isParent() => check parents
        # héritage sans modifier parent
        # if depth == 0:
        #     return
        for ligne in range(parent.size):
            for colonne in range (parent.size):
                if parent.data[ligne][colonne] == '.':
                    child = Node(deepcopy(parent.data), parent.size)
                    child.data[ligne][colonne] = value
                    child.playedCase = Case(ligne, colonne)
                    if child not in parent.next:
                        parent.next.append(child)
                        # _copyValue = copy(value)
                        # if value == 1:
                        #     _copyValue = 2
                        # else:
                        #     _copyValue = 1
                        # self.createNode(child, _copyValue, depth - 1)
    
>>>>>>> de3df6ff88097530f77fb9ff5f0ef2e653c421d4

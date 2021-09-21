from concurrent.futures import ProcessPoolExecutor

class Piece:
    def __init__(self, name, side, f, w):
        self.name = name
        self.side = side
        self.firstMove = f
        self.worth = w
        self.possMoves = []
        self.alive = True

    def printPoss(self):
        print(self.side, self.name, ": ", end='')
        for p in self.possMoves:
            print("[", p[1], " ", p[0], "]", end='')
        print()


class boardPiece:
    def __init__(self, name, side, f, w):
        if name is None:
            self.piece = None
        else:
            self.piece = Piece(name, side, f, w)

    def returncopy(self):
        if self.piece is None:
            copy_object = boardPiece(None, None, None, None)
            return copy_object
        else:
            copy_object = boardPiece(self.piece.name, self.piece.side, self.piece.firstMove, self.piece.worth)
            for poss in self.piece.possMoves:
                copy_object.piece.possMoves.append([poss[0], poss[1]])
            return copy_object


class chessBoard:
    def __init__(self, PlayerSide):
        self.playerside = PlayerSide

        if self.playerside == "White":
            self.board = [[boardPiece("Rook", "Black", True, -5), boardPiece("Knight", "Black", True, -3),
                           boardPiece("Bishop", "Black", True, -3), boardPiece("Queen", "Black", True, -10),
                           boardPiece("King", "Black", True, -99), boardPiece("Bishop", "Black", True, -3),
                           boardPiece("Knight", "Black", True, -3), boardPiece("Rook", "Black", True, -5)],
                          [boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1),
                           boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1),
                           boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1),
                           boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1),
                           boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1),
                           boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1),
                           boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1)],
                          [boardPiece("Rook", "White", True, 5), boardPiece("Knight", "White", True, 3),
                           boardPiece("Bishop", "White", True, 3), boardPiece("Queen", "White", True, 10),
                           boardPiece("King", "White", True, 99), boardPiece("Bishop", "White", True, 3),
                           boardPiece("Knight", "White", True, 3), boardPiece("Rook", "White", True, 5)]]

        else:
            self.board = [[boardPiece("Rook", "White", True, 5), boardPiece("Knight", "White", True, 3),
                           boardPiece("Bishop", "White", True, 3), boardPiece("Queen", "White", True, 10),
                           boardPiece("King", "White", True, 99), boardPiece("Bishop", "White", True, 3),
                           boardPiece("Knight", "White", True, 3), boardPiece("Rook", "White", True, 5)],
                          [boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1),
                           boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1),
                           boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1),
                           boardPiece("Pawn", "White", True, 1), boardPiece("Pawn", "White", True, 1)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0),
                           boardPiece(None, None, None, 0), boardPiece(None, None, None, 0)],
                          [boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1),
                           boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1),
                           boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1),
                           boardPiece("Pawn", "Black", True, -1), boardPiece("Pawn", "Black", True, -1)],
                          [boardPiece("Rook", "Black", True, -5), boardPiece("Knight", "Black", True, -3),
                           boardPiece("Bishop", "Black", True, -3), boardPiece("Queen", "Black", True, -10),
                           boardPiece("King", "Black", True, -99), boardPiece("Bishop", "Black", True, -3),
                           boardPiece("Knight", "Black", True, -3), boardPiece("Rook", "Black", True, -5)]]

        self.side = "White"
        self.wCheckmated = False
        self.bCheckmated = False

    def returncopy(self):
        copy_object = chessBoard(self.playerside)
        copy_object.side = self.side
        copy_object.wCheckmated = self.wCheckmated
        copy_object.bCheckmated = self.bCheckmated
        for y in range(8):
            for x in range(8):
                copy_object.board[y][x] = self.board[y][x].returncopy()

        return copy_object

    def movePiece(self, y1, x1, y2, x2):
        if self.board[y1][x1].piece is not None:
            if (y2 == 0 or y2 == 7) and self.board[y1][x1].piece.name == "Pawn":
                if self.board[y1][x1].piece.side == "White":
                    self.board[y2][x2].piece = Piece("Queen", self.board[y1][x1].piece.side, False, 10)
                else:
                    self.board[y2][x2].piece = Piece("Queen", self.board[y1][x1].piece.side, False, -10)
            else:
                self.board[y1][x1].piece.firstMove = False
                if self.board[y2][x2].piece is not None:
                    self.board[y2][x2].piece.alive = False
                    if self.board[y2][x2].piece.name == "King":
                        if self.board[y2][x2].piece.side == "White":
                            self.wCheckmated = True
                        else:
                            self.bCheckmated = True
                self.board[y2][x2].piece = self.board[y1][x1].piece
                if self.board[y1][x1].piece.name == "King":
                    if x2 - x1 == 2:
                        if self.board[y1][7].piece is not None:
                            self.board[y1][7].piece.firstMove = False
                        self.board[y2][5].piece = self.board[y1][7].piece
                        self.board[y1][7].piece = None
                    elif x2 - x1 == -2:
                        if self.board[y1][0].piece is not None:
                            self.board[y1][0].piece.firstMove = False
                        self.board[y2][3].piece = self.board[y1][0].piece
                        self.board[y1][0].piece = None
            self.board[y1][x1].piece = None
        self.updatePoss()
        self.flipSides()

    def updatePieceMoves(self, y, x):
        if self.board[y][x].piece.name == "Pawn":
            if self.playerside == "White":
                if self.board[y][x].piece.side == "White":
                    if y - 1 >= 0:
                        if self.board[y - 1][x].piece is None:
                            if y - 2 >= 0:
                                if self.board[y - 2][x].piece is None and self.board[y][x].piece.firstMove:
                                    self.board[y][x].piece.possMoves.append([y - 2, x])
                            self.board[y][x].piece.possMoves.append([y - 1, x])
                        if x - 1 >= 0:
                            if self.board[y - 1][x - 1].piece is not None:
                                if self.board[y - 1][x - 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y - 1, x - 1])
                        if x + 1 < 8:
                            if self.board[y - 1][x + 1].piece is not None:
                                if self.board[y - 1][x + 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y - 1, x + 1])
                else:
                    if y + 1 < 8:
                        if self.board[y + 1][x].piece is None:
                            if y + 2 < 8:
                                if self.board[y + 2][x].piece is None and self.board[y][x].piece.firstMove:
                                    self.board[y][x].piece.possMoves.append([y + 2, x])
                            self.board[y][x].piece.possMoves.append([y + 1, x])
                        if x - 1 >= 0:
                            if self.board[y + 1][x - 1].piece is not None:
                                if self.board[y + 1][x - 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y + 1, x - 1])
                        if x + 1 < 8:
                            if self.board[y + 1][x + 1].piece is not None:
                                if self.board[y + 1][x + 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y + 1, x + 1])
            else:
                if self.board[y][x].piece.side == "Black":
                    if y - 1 >= 0:
                        if self.board[y - 1][x].piece is None:
                            if y - 2 >= 0:
                                if self.board[y - 2][x].piece is None and self.board[y][x].piece.firstMove:
                                    self.board[y][x].piece.possMoves.append([y - 2, x])
                            self.board[y][x].piece.possMoves.append([y - 1, x])
                        if x - 1 >= 0:
                            if self.board[y - 1][x - 1].piece is not None:
                                if self.board[y - 1][x - 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y - 1, x - 1])
                        if x + 1 < 8:
                            if self.board[y - 1][x + 1].piece is not None:
                                if self.board[y - 1][x + 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y - 1, x + 1])
                else:
                    if y + 1 < 8:
                        if self.board[y + 1][x].piece is None:
                            if y + 2 < 8:
                                if self.board[y + 2][x].piece is None and self.board[y][x].piece.firstMove:
                                    self.board[y][x].piece.possMoves.append([y + 2, x])
                            self.board[y][x].piece.possMoves.append([y + 1, x])
                        if x - 1 >= 0:
                            if self.board[y + 1][x - 1].piece is not None:
                                if self.board[y + 1][x - 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y + 1, x - 1])
                        if x + 1 < 8:
                            if self.board[y + 1][x + 1].piece is not None:
                                if self.board[y + 1][x + 1].piece.side != self.board[y][x].piece.side:
                                    self.board[y][x].piece.possMoves.append([y + 1, x + 1])

        if self.board[y][x].piece.name == "Rook" or self.board[y][x].piece.name == "Queen":
            up = False
            down = False
            left = False
            right = False
            for i in range(1, 8):
                if y - i >= 0 and not up:
                    if self.board[y - i][x].piece is None:
                        self.board[y][x].piece.possMoves.append([y - i, x])
                    else:
                        up = True
                        if self.board[y - i][x].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y - i, x])
                if y + i < 8 and not down:
                    if self.board[y + i][x].piece is None:
                        self.board[y][x].piece.possMoves.append([y + i, x])
                    else:
                        down = True
                        if self.board[y + i][x].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y + i, x])
                if x - i >= 0 and not left:
                    if self.board[y][x - i].piece is None:
                        self.board[y][x].piece.possMoves.append([y, x - i])
                    else:
                        left = True
                        if self.board[y][x - i].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y, x - i])
                if x + i < 8 and not right:
                    if self.board[y][x + i].piece is None:
                        self.board[y][x].piece.possMoves.append([y, x + i])
                    else:
                        right = True
                        if self.board[y][x + i].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y, x + i])

        if self.board[y][x].piece.name == "Bishop" or self.board[y][x].piece.name == "Queen":
            topLeft = False
            topRight = False
            bottomRight = False
            bottomLeft = False
            for i in range(1, 8):
                if y - i >= 0 and x - i >= 0 and not topLeft:
                    if self.board[y - i][x - i].piece is None:
                        self.board[y][x].piece.possMoves.append([y - i, x - i])
                    else:
                        topLeft = True
                        if self.board[y - i][x - i].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y - i, x - i])
                if y - i >= 0 and x + i < 8 and not topRight:
                    if self.board[y - i][x + i].piece is None:
                        self.board[y][x].piece.possMoves.append([y - i, x + i])
                    else:
                        topRight = True
                        if self.board[y - i][x + i].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y - i, x + i])
                if y + i < 8 and x + i < 8 and not bottomRight:
                    if self.board[y + i][x + i].piece is None:
                        self.board[y][x].piece.possMoves.append([y + i, x + i])
                    else:
                        bottomRight = True
                        if self.board[y + i][x + i].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y + i, x + i])
                if y + i < 8 and x - i >= 0 and not bottomLeft:
                    if self.board[y + i][x - i].piece is None:
                        self.board[y][x].piece.possMoves.append([y + i, x - i])
                    else:
                        bottomLeft = True
                        if self.board[y + i][x - i].piece.side != self.board[y][x].piece.side:
                            self.board[y][x].piece.possMoves.append([y + i, x - i])

        if self.board[y][x].piece.name == "Knight":
            if x - 2 >= 0 and y - 1 >= 0:
                if self.board[y - 1][x - 2].piece is None:
                    self.board[y][x].piece.possMoves.append([y - 1, x - 2])
                else:
                    if self.board[y - 1][x - 2].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y - 1, x - 2])
            if x - 1 >= 0 and y - 2 >= 0:
                if self.board[y - 2][x - 1].piece is None:
                    self.board[y][x].piece.possMoves.append([y - 2, x - 1])
                else:
                    if self.board[y - 2][x - 1].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y - 2, x - 1])
            if x + 2 < 8 and y + 1 < 8:
                if self.board[y + 1][x + 2].piece is None:
                    self.board[y][x].piece.possMoves.append([y + 1, x + 2])
                else:
                    if self.board[y + 1][x + 2].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y + 1, x + 2])
            if x + 1 < 8 and y + 2 < 8:
                if self.board[y + 2][x + 1].piece is None:
                    self.board[y][x].piece.possMoves.append([y + 2, x + 1])
                else:
                    if self.board[y + 2][x + 1].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y + 2, x + 1])
            if x + 2 < 8 and y - 1 >= 0:
                if self.board[y - 1][x + 2].piece is None:
                    self.board[y][x].piece.possMoves.append([y - 1, x + 2])
                else:
                    if self.board[y - 1][x + 2].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y - 1, x + 2])
            if x + 1 < 8 and y - 2 >= 0:
                if self.board[y - 2][x + 1].piece is None:
                    self.board[y][x].piece.possMoves.append([y - 2, x + 1])
                else:
                    if self.board[y - 2][x + 1].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y - 2, x + 1])
            if x - 2 >= 0 and y + 1 < 8:
                if self.board[y + 1][x - 2].piece is None:
                    self.board[y][x].piece.possMoves.append([y + 1, x - 2])
                else:
                    if self.board[y + 1][x - 2].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y + 1, x - 2])
            if x - 1 >= 0 and y + 2 < 8:
                if self.board[y + 2][x - 1].piece is None:
                    self.board[y][x].piece.possMoves.append([y + 2, x - 1])
                else:
                    if self.board[y + 2][x - 1].piece.side != self.board[y][x].piece.side:
                        self.board[y][x].piece.possMoves.append([y + 2, x - 1])

        if self.board[y][x].piece.name == "King":
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if i != 0 or j != 0:
                        if 0 <= y + i < 8 and 0 <= x + j < 8:
                            if self.board[y + i][x + j].piece is None:
                                self.board[y][x].piece.possMoves.append([y + i, x + j])
                            elif self.board[y + i][x + j].piece.side != self.board[y][x].piece.side:
                                self.board[y][x].piece.possMoves.append([y + i, x + j])

            if self.board[y][x].piece.firstMove:
                if self.board[y][x + 3].piece is not None and self.board[y][x + 2].piece is None and \
                        self.board[y][x + 1].piece is None:
                    if self.board[y][7].piece.name == "Rook" and self.board[y][7].piece.firstMove:
                        self.board[y][x].piece.possMoves.append([y, x + 2])
                if self.board[y][x - 4].piece is not None and self.board[y][x - 3].piece is None and \
                        self.board[y][x - 2].piece is None and self.board[y][x - 1].piece is None:
                    if self.board[y][0].piece.name == "Rook" and self.board[y][0].piece.firstMove:
                        self.board[y][x].piece.possMoves.append([y, x - 2])

    def updatePoss(self):
        for y in range(8):
            for x in range(8):
                if self.board[y][x].piece is not None:
                    if self.board[y][x].piece.alive:
                        self.board[y][x].piece.possMoves.clear()
                        self.updatePieceMoves(y, x)

    def flipSides(self):
        if self.side == "White":
            self.side = "Black"
        else:
            self.side = "White"

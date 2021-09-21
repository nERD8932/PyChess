import baseClasses as bcs
from concurrent.futures import ProcessPoolExecutor
from time import process_time


class Node:
    def __init__(self, cb: bcs.chessBoard, moveset, py, px, h):
        self.cb = cb
        self.moveset = moveset
        self.py = py
        self.px = px
        self.heu = h

    def calcheuristic(self):
        h = 0
        for y in range(8):
            for x in range(8):
                if self.cb.board[y][x].piece is not None:
                    h += self.cb.board[y][x].piece.worth
                    h += (len(self.cb.board[y][x].piece.possMoves) / 16) * self.cb.board[y][x].piece.worth
        self.heu = h

    def printinfo(self):
        print("Heuristic: ", self.heu, " Moveset:", self.moveset, " Parents: [", self.py, ", ", self.px, "]")

    def returncopy(self):
        copy_object = Node(self.cb.returncopy(), [], self.py, self.px, self.heu)
        for x in self.moveset:
            copy_object.moveset.append(x)

        return copy_object


def calcheuristic_multithread(node):
    h = 0
    for y in range(8):
        for x in range(8):
            if node.cb.board[y][x].piece is not None:
                h += node.cb.board[y][x].piece.worth
                if node.cb.board[y][x].piece.name != "King":
                    h += (len(node.cb.board[y][x].piece.possMoves) / 25) * node.cb.board[y][x].piece.worth
    return h


def returnChildNodes(cb: bcs.chessBoard, depth, n):
    childnodes = []
    for y in range(8):
        for x in range(8):
            if cb.board[y][x].piece is not None:
                if cb.board[y][x].piece.side == cb.side:
                    for poss in cb.board[y][x].piece.possMoves:
                        tempcb = cb.returncopy()
                        tempcb.movePiece(y, x, poss[0], poss[1])
                        if tempcb.side == "White":
                            childnodes.append(Node(tempcb, [y, x, poss[0], poss[1]], depth, n, -999))
                        else:
                            childnodes.append(Node(tempcb, [y, x, poss[0], poss[1]], depth, n, 999))
    return childnodes


def returnChildNodes_multithread(args):
    childnodes = []
    for y in range(8):
        for x in range(8):
            if args[0].board[y][x].piece is not None:
                if args[0].board[y][x].piece.side == args[0].side:
                    for poss in args[0].board[y][x].piece.possMoves:
                        tempcb = args[0].returncopy()
                        tempcb.movePiece(y, x, poss[0], poss[1])
                        if tempcb.side == "White":
                            childnodes.append(Node(tempcb, [y, x, poss[0], poss[1]], args[1], args[2], -999))
                        else:
                            childnodes.append(Node(tempcb, [y, x, poss[0], poss[1]], args[1], args[2], 999))
    return childnodes


def gentree_multithread(cb: bcs.chessBoard, depthLim):
    if cb.side == "White":
        tempNode = Node(cb, None, None, None, -999)
    else:
        tempNode = Node(cb, None, None, None, 999)
    nodeTree = [[tempNode], []]

    leafnodes = returnChildNodes(cb, 0, 0)
    for x in leafnodes:
        nodeTree[1].append(x.returncopy())

    args = []
    leafnodes = []

    # starttime = process_time()

    for depth in range(1, depthLim):
        args.clear()
        leafnodes.clear()
        for n in range(len(nodeTree[depth])):
            args.append([nodeTree[depth][n].cb, depth, n])
        with ProcessPoolExecutor() as executor:
            for result in executor.map(returnChildNodes_multithread, args, chunksize=20):
                leafnodes.extend(result)
        nodeTree.append([])
        for x in leafnodes:
            nodeTree[depth+1].append(x.returncopy())

    # print("First Loop: ", process_time() - starttime)
    #
    # starttime = process_time()

    with ProcessPoolExecutor() as executor:
        for n, result in zip(nodeTree[depthLim], executor.map(calcheuristic_multithread, nodeTree[depthLim], chunksize=20)):
            n.heu = result

    # print("Second Loop: ", process_time() - starttime)
    #
    # starttime = process_time()

    for depth in range(depthLim, 0, -1):
        if nodeTree[depth - 1][0].cb.side == "White":
            for n in nodeTree[depth]:
                if n.heu >= nodeTree[n.py][n.px].heu:
                    nodeTree[n.py][n.px].heu = n.heu
        elif nodeTree[depth - 1][0].cb.side == "Black":
            for n in nodeTree[depth]:
                if n.heu <= nodeTree[n.py][n.px].heu:
                    nodeTree[n.py][n.px].heu = n.heu

    # print("Third Loop: ", process_time() - starttime)
    #
    # starttime = process_time()

    if nodeTree[0][0].cb.side == "White":
        for n in nodeTree[1]:
            if n.heu >= nodeTree[0][0].heu:
                nodeTree[0][0].moveset = n.moveset
    elif nodeTree[0][0].cb.side == "Black":
        for n in nodeTree[1]:
            if n.heu <= nodeTree[0][0].heu:
                nodeTree[0][0].moveset = n.moveset

    # print("Fourth Loop: ", process_time() - starttime, "\n\n")

    return nodeTree[0][0].moveset


def genTree(cb: bcs.chessBoard, depthLim):
    if cb.side == "White":
        tempNode = Node(cb, None, None, None, -999)
    else:
        tempNode = Node(cb, None, None, None, 999)
    nodeTree = [[tempNode.returncopy()]]
    for depth in range(depthLim):
        leafNodes = []
        for n in range(len(nodeTree[depth])):
            leafNodes.extend(returnChildNodes(nodeTree[depth][n].cb, depth, n))

        nodeTree.append([x.returncopy for x in leafNodes])

    for n in nodeTree[depthLim - 1]:
        n.calcheuristic()

    for depth in range(depthLim - 1, 0, -1):
        if nodeTree[depth - 1][0].cb.side == "White":
            for n in nodeTree[depth]:
                if n.heu >= nodeTree[n.py][n.px].heu:
                    nodeTree[n.py][n.px].heu = n.heu
        elif nodeTree[depth - 1][0].cb.side == "Black":
            for n in nodeTree[depth]:
                if n.heu <= nodeTree[n.py][n.px].heu:
                    nodeTree[n.py][n.px].heu = n.heu

    if nodeTree[0][0].cb.side == "White":
        for n in nodeTree[1]:
            if n.heu >= nodeTree[0][0].heu:
                nodeTree[0][0].moveset = n.moveset
    elif nodeTree[0][0].cb.side == "Black":
        for n in nodeTree[1]:
            if n.heu <= nodeTree[0][0].heu:
                nodeTree[0][0].moveset = n.moveset

    return nodeTree[0][0].moveset

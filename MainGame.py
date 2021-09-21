import pygame
from sys import exit
from math import ceil, isclose
from time import sleep, process_time

from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)

import baseClasses as bcs
from MinMaxAI import gentree_multithread

DEPTHLIM = 2


class Game:
    def __init__(self, startside):
        pygame.display.set_caption("PyChess")
        self.running = True
        self.startside = startside
        self.game = ChessGame(startside)

    def runGame(self):
        if self.game.aiEnabled and self.startside == "Black":
            self.game.renderDisplay(None)
            aimove = gentree_multithread(self.game.cb, DEPTHLIM)
            self.game.renderDisplay([aimove[0], aimove[1], aimove[2], aimove[3]])
            self.game.cb.movePiece(aimove[0], aimove[1], aimove[2], aimove[3])
        while self.running:
            self.game.renderDisplay(None)
            self.checkEvents()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                self.game.convertMouseInput(event.pos)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == QUIT:
                self.running = False


class ChessGame:
    def __init__(self, PlayerSide):
        pygame.init()
        screeninfo = pygame.display.Info()
        self.resfactor = int(screeninfo.current_h * 1)
        self.boardedge = int((self.resfactor - 41.1428) / 22.8571)
        self.pieceedge = int((self.resfactor - 38.7364) / 8.4210)
        self.screen = pygame.Surface([1024, 1024])
        self.display = pygame.display.set_mode([self.resfactor, self.resfactor])
        self.clock = pygame.time.Clock()
        self.cb = bcs.chessBoard(PlayerSide)
        self.cb.updatePoss()
        self.selected = False
        self.aiEnabled = True
        pygame.display.set_icon(pygame.image.load("sprites/icon.png"))
        self.bg = pygame.image.load("sprites/BG.png").convert()
        self.s_img = pygame.image.load("sprites/selection.png").convert_alpha()
        self.s_img.set_alpha(100)
        self.w_winner = pygame.image.load("sprites/whitewins.png").convert_alpha()
        self.b_winner = pygame.image.load("sprites/blackwins.png").convert_alpha()

    def convertMouseInput(self, mpos):
        if self.selected:
            self.origiy = self.my
            self.origix = self.mx
        self.mx, self.my = mpos
        if self.mx in range(self.boardedge, self.resfactor - self.boardedge) and \
                self.my in range(self.boardedge, self.resfactor - self.boardedge):
            self.mx = int((self.mx - self.boardedge) / self.pieceedge)
            self.my = int((self.my - self.boardedge) / self.pieceedge)
            # print("Clicked [ Y = ", self.my, ", X = ", self.mx, "]\n")
            if not self.selected and \
                    self.cb.board[self.my][self.mx].piece is not None and \
                    0 <= self.mx <= 7 and 0 <= self.my <= 7:
                if self.cb.board[self.my][self.mx].piece.side == self.cb.side:
                    self.selected = True
            elif 0 <= self.mx <= 7 and 0 <= self.my <= 7:
                if self.cb.board[self.origiy][self.origix].piece is not None:
                    if [self.my, self.mx] in self.cb.board[self.origiy][self.origix].piece.possMoves:
                        self.selected = False
                        self.renderDisplay([self.origiy, self.origix, self.my, self.mx])
                        self.cb.movePiece(self.origiy, self.origix, self.my, self.mx)
                        self.renderDisplay(None)
                        if self.aiEnabled and not (self.cb.bCheckmated and self.cb.wCheckmated):
                            # start = time.process_time()
                            aimove = gentree_multithread(self.cb, DEPTHLIM)
                            # print(time.process_time() - start)
                            self.renderDisplay([aimove[0], aimove[1], aimove[2], aimove[3]])
                            self.cb.movePiece(aimove[0], aimove[1], aimove[2], aimove[3])
                    elif self.cb.board[self.my][self.mx].piece is not None:
                        if self.cb.board[self.my][self.mx].piece.side != self.cb.side:
                            self.selected = False

    def renderDisplay(self, move):
        if move is None:
            self.screen.blit(self.bg, (0, 0))
            for y in range(8):
                for x in range(8):
                    if self.cb.board[y][x].piece is not None:
                        p_img = pygame.image.load("sprites/" + self.cb.board[y][x].piece.side +
                                                  self.cb.board[y][x].piece.name + ".png").convert_alpha()
                        self.screen.blit(p_img,
                                         (self.returnEdge(0.048828) + x * self.returnEdge(0.115),
                                          self.returnEdge(0.048828) + y * self.returnEdge(0.115)))
            if self.selected and 0 <= self.my < 8 and 0 <= self.mx < 8:
                if self.cb.board[self.my][self.mx].piece is not None:
                    for poss in self.cb.board[self.my][self.mx].piece.possMoves:
                        self.screen.blit(self.s_img,
                                         ((poss[1] * self.returnEdge(0.115)) + self.returnEdge(0.039),
                                          (poss[0] * self.returnEdge(0.115)) + self.returnEdge(0.039)))
            else:
                self.selected = False
            frame = pygame.transform.scale(self.screen, (self.resfactor, self.resfactor))
            self.display.blit(frame, frame.get_rect())
            pygame.display.flip()
            self.clock.tick(120)
        else:
            dy = (move[2] - move[0]) / 10
            dx = (move[3] - move[1]) / 10
            inity = move[0]
            initx = move[1]

            while (not isclose(inity, move[2], abs_tol=10 ** -2)) or (not isclose(initx, move[3], abs_tol=10 ** -2)):
                self.screen.blit(self.bg, (0, 0))
                for y in range(8):
                    for x in range(8):
                        if self.cb.board[y][x].piece is not None and (y != move[0] or x != move[1]):
                            p_img = pygame.image.load("sprites/" + self.cb.board[y][x].piece.side +
                                                      self.cb.board[y][x].piece.name + ".png").convert_alpha()
                            self.screen.blit(p_img,
                                             (self.returnEdge(0.048828) + x * self.returnEdge(0.1152),
                                              self.returnEdge(0.048828) + y * self.returnEdge(0.1152)))
                inity += dy
                initx += dx
                p_img = pygame.image.load("sprites/" + self.cb.board[move[0]][move[1]].piece.side +
                                          self.cb.board[move[0]][move[1]].piece.name + ".png").convert_alpha()
                self.screen.blit(p_img,
                                 (self.returnEdge(0.048828) + initx * self.returnEdge(0.1152),
                                  self.returnEdge(0.048828) + inity * self.returnEdge(0.1152)))
                frame = pygame.transform.scale(self.screen,
                                               (self.resfactor,
                                                self.resfactor))
                self.display.blit(frame, frame.get_rect())
                pygame.display.flip()
                self.clock.tick(60)

        if self.cb.bCheckmated:
            self.screen.blit(self.w_winner, (0, 0))
            frame = pygame.transform.scale(self.screen,
                                           (self.resfactor,
                                            self.resfactor))
            self.display.blit(frame, frame.get_rect())
            pygame.display.flip()
            sleep(5)
            pygame.quit()
            exit(1)

        elif self.cb.wCheckmated:
            self.screen.blit(self.b_winner, (0, 0))
            frame = pygame.transform.scale(self.screen,
                                           (self.resfactor,
                                            self.resfactor))
            self.display.blit(frame, frame.get_rect())
            pygame.display.flip()
            sleep(5)
            pygame.quit()
            exit(1)

    def returnEdge(self, x):
        return ceil(self.resfactor * x * (1024 / self.resfactor))

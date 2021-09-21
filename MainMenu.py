from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import MainGame
from math import ceil

from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyChess")
        pygame.display.set_icon(pygame.image.load("sprites/icon.png"))
        screeninfo = pygame.display.Info()
        self.resfactor = int(screeninfo.current_h * 0.94)
        self.screen = pygame.Surface([1024, 1024])
        self.display = pygame.display.set_mode([self.resfactor, self.resfactor])
        self.running = True
        self.mouseinput = None
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("sprites/mainmenu.png")
        self.selectionWhite = pygame.image.load("sprites/white_menusetting.png")
        self.selectionBlack = pygame.image.load("sprites/black_menusetting.png")
        self.selectionsprite = pygame.image.load("sprites/menuselection.png").convert_alpha()
        self.buttonRange = [self.returnEdge(0.21875),
                            self.returnEdge(0.434570),
                            self.returnEdge(0.546875),
                            self.returnEdge(0.659179),
                            self.returnEdge(0.771484),
                            self.returnEdge(0.39746),
                            self.returnEdge(0.64746),
                            self.returnEdge(0.68554),
                            self.returnEdge(0.93554),
                            self.returnEdge(0.83691),
                            self.returnEdge(0.93066)]
        self.startingside = "White"

    def runMenu(self):
        while self.running:
            self.renderDisplay()
            self.checkEvents()
            self.clock.tick(60)

    def renderDisplay(self):
        self.screen.blit(self.bg, (0, 0))
        if self.startingside == "White":
            self.screen.blit(self.selectionsprite, (self.buttonRange[5], self.buttonRange[9]))
        else:
            self.screen.blit(self.selectionsprite, (self.buttonRange[7], self.buttonRange[9]))
        self.screen.blit(self.selectionWhite, (self.buttonRange[5], self.buttonRange[9]))
        self.screen.blit(self.selectionBlack, (self.buttonRange[7], self.buttonRange[9]))
        frame = pygame.transform.scale(self.screen, (self.resfactor, self.resfactor))
        self.display.blit(frame, frame.get_rect())
        pygame.display.flip()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                self.mouseinput = event.pos
                if self.mouseinput[0] in range(self.buttonRange[0], self.resfactor - self.buttonRange[0]) and \
                        self.mouseinput[1] in range(self.buttonRange[1], self.buttonRange[2]):
                    gameexec = MainGame.Game(self.startingside)
                    gameexec.game.aiEnabled = False
                    gameexec.runGame()
                elif self.mouseinput[0] in range(self.buttonRange[0], self.resfactor - self.buttonRange[0]) and \
                        self.mouseinput[1] in range(self.buttonRange[2], self.buttonRange[3]):
                    exe = MainGame.Game(self.startingside)
                    exe.game.aiEnabled = True
                    exe.runGame()
                elif self.mouseinput[0] in range(self.buttonRange[0], self.resfactor - self.buttonRange[0]) and \
                        self.mouseinput[1] in range(self.buttonRange[3], self.buttonRange[4]):
                    self.running = False
                elif self.mouseinput[0] in range(self.buttonRange[5], self.buttonRange[6]) and \
                        self.mouseinput[1] in range(self.buttonRange[9], self.buttonRange[10]):
                    self.startingside = "White"
                elif self.mouseinput[0] in range(self.buttonRange[7], self.buttonRange[8]) and \
                        self.mouseinput[1] in range(self.buttonRange[9], self.buttonRange[10]):
                    self.startingside = "Black"
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == QUIT:
                self.running = False

    def returnEdge(self, x):
        return ceil(self.resfactor * x * (1024 / self.resfactor))

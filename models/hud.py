#!/usr/bin/python

__version__ = "1.0.0"
__author__ = "Valentin 'Ookamiko' Dewilde"

import pygame

class Hud:
    SCR_COLOR = (255, 255, 255)
    DEFAULT_BCKG = (0, 0, 0)

    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("arial", 20)
        self.surface = None

    def link_parent(self, subsurface):
        self.surface = subsurface
        self.update_hud()

    def update_hud(self):
        self.surface.fill(self.DEFAULT_BCKG)
        score = self.font.render(
            "Your Score: " + str(self.score), 
            True, self.SCR_COLOR)
        self.surface.blit(score, [10, 10])

    def increase_score(self, point):
        self.score += point
        self.update_hud()

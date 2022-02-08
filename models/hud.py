#!/usr/bin/python

__version__ = "1.0.0"
__author__ = "Valentin 'Ookamiko' Dewilde"

import pygame

class Hud:
    SCR_COLOR = (255, 255, 255)
    DEFAULT_BCKG = (0, 0, 0)

    def __init__(self, use_ai=False, gen=None, org=None):
        self.score = 0
        self.font = pygame.font.SysFont("arial", 20)
        self.surface = None
        self.use_ai = use_ai

        if use_ai:
            self.step = 0
            self.generation = gen
            self.organism = org

    def link_parent(self, subsurface):
        self.surface = subsurface
        self.update_hud()

    def update_hud(self):
        self.surface.fill(self.DEFAULT_BCKG)
        score = self.font.render(
            "Your Score: " + str(self.score), 
            True, self.SCR_COLOR)
        self.surface.blit(score, [10, 10])

        if self.use_ai:
            step_left = self.font.render(
                "Step left: " + str(self.step),
                True, self.SCR_COLOR)
            self.surface.blit(step_left, [140, 10])

            gen_txt = self.font.render(
                "Gen: " + str(self.generation),
                True, self.SCR_COLOR)
            self.surface.blit(gen_txt, [10, 30])

            org_txt = self.font.render(
                "Individu: " + str(self.organism),
                True, self.SCR_COLOR)
            self.surface.blit(org_txt, [140, 30])

    def increase_score(self, point):
        self.score += point
        self.update_hud()

    def update_step_left(self, step):
        self.step = step
        self.update_hud()

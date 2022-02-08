#!/usr/bin/python

__version__ = "1.0.0"
__author__ = "Valentin 'Ookamiko' Dewilde"

import pygame
import os
import numpy as np

from models.snake import Snake
from models.hud import Hud
from models.arena import Arena


class Board:
    HUD_HEIGHT = 50
    DEFAULT_BCKG = (0, 0, 0)
    FONT_COLOR = (255, 255, 255)

    def __init__(self, caption, arena_size, use_ai=False):

        pygame.init()

        self.font = pygame.font.SysFont("Arial", 20)
        self.arena = Arena(arena_size, use_ai=use_ai)
        self.hud = Hud(use_ai=use_ai)
        self.use_ai = use_ai

        if use_ai:
            self.apple_take = 0
            self.move_left = 100
            self.move_made = 0
            self.hud.step = 100

        self.window = pygame.display.set_mode(
            (max(247, self.arena.get_width() + 20),
             max(297, self.arena.get_height() + 70)))

        self.arena.link_parent(
            self.window.subsurface(
                [10,
                 self.HUD_HEIGHT + 10,
                 self.arena.get_width(),
                 self.arena.get_height()]
        ))
        self.arena.generate_apple()
        self.arena.display_arena()

        self.hud.link_parent(
            self.window.subsurface(
                [0, 0, self.window.get_width(), self.HUD_HEIGHT]
        ))

        pygame.display.update()
        pygame.display.set_caption(caption)

    def reset(self, generation=None, organism=None):

        self.window.fill(self.DEFAULT_BCKG)

        self.arena = Arena(self.arena.size, use_ai=self.use_ai)
        self.arena.link_parent(
            self.window.subsurface(
                [10,
                 self.HUD_HEIGHT + 10,
                 self.arena.get_width(),
                 self.arena.get_height()]
        ))
        self.arena.generate_apple()
        self.arena.display_arena()

        self.hud = Hud(use_ai=self.use_ai, gen=generation, org=organism)
        self.hud.link_parent(
            self.window.subsurface(
                [0, 0, self.window.get_width(), self.HUD_HEIGHT]
        ))

        if self.use_ai:
            self.apple_take = 0
            self.move_made = 0
            self.move_left = self.arena.size**2
            self.hud.update_step_left(self.move_left)

        pygame.display.update()

    def render_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.arena.snake.update_move_modif(Snake.M_UP)
            elif event.key == pygame.K_DOWN:
                self.arena.snake.update_move_modif(Snake.M_DOWN)
            elif event.key == pygame.K_LEFT:
                self.arena.snake.update_move_modif(Snake.M_LEFT)
            elif event.key == pygame.K_RIGHT:
                self.arena.snake.update_move_modif(Snake.M_RIGHT)

    def next_step(self):
        # Move snake
        tail_pos = self.arena.snake.move_snake()
        if self.use_ai:
            self.move_left -= 1
            self.move_made += 1

        # Check lose
        if self.arena.has_lose() or (self.use_ai and self.move_left == 0):
            self.arena.snake.snake_pos.pop(0)
            self.arena.display_arena()
            pygame.display.update()
            return True

        # Check apple
        if self.arena.has_get_apple():
            self.arena.snake.increase(tail_pos)
            self.arena.generate_apple()
            self.hud.increase_score(Arena.APPLE_POINT)

            if self.use_ai:
                self.move_left += self.arena.size**2 * 0.75
                self.apple_take += 1

        self.hud.update_step_left(self.move_left)
        self.arena.display_arena()
        pygame.display.update()

        return False

    def display_game_over(self):
        
        game_over_lines = [
            self.font.render("Your score: " + str(self.hud.score), 
                True, self.FONT_COLOR),
            self.font.render("You lose",
                True, self.FONT_COLOR),
            self.font.render("Press R to restart or Q to exit",
                True, self.FONT_COLOR)
        ]

        for count, line in enumerate(game_over_lines):
            center_pos = (self.window.get_width()/2,
                self.window.get_height()/2 - 100 + count*20)
            self.window.blit(line, line.get_rect(center=center_pos))
            
        pygame.display.update()

    def get_fitness(self):
        return max(0.0001, self.move_made
            + (2**self.apple_take + (self.apple_take**2.1) * 500)
            - (self.apple_take**1.2 * (0.25*self.move_made)**1.3))

    def save_stats(self, stats, gen, file="stats.txt"):
        if not(os.path.exists("stats\\" + file)):
            f = open("stats\\" + file, "w")
            f.write("|Max Apple|Mean Apple|Max Step|Mean Step|" +
                "Max Fitness|Mean Fitness\n")
            f.close()

        f = open("stats\\" + file, "a")

        f.write("Generation " + str(gen) + "|" +
            str(np.max(stats["apple"])) + "|" +
            str(np.mean(stats["apple"])) + "|" +
            str(np.max(stats["step"])) + "|" +
            str(np.mean(stats["step"])) + "|" +
            str(np.max(stats["fitness"])) + "|" +
            str(np.mean(stats["fitness"])) + "\n")

        f.close()

#!/usr/bin/python

__version__ = "1.0.0"
__author__ = "Valentin 'Ookamiko' Dewilde"

import pygame
import random

from models.snake import Snake


class Arena:
    ASQR_SIZE = 15
    TILE_SIZE = 15
    BDR_SIZE = 1
    BDR_COLOR = SNAKE_COLOR = (255, 255, 255)
    APPLE_COLOR = (255, 0, 0)
    DEFAULT_BCKG = (0, 0, 0)
    APPLE_POINT = 10

    def __init__(self, size):
        self.size = max(size, 5)
        self.apple_pos = -1
        self.apple_asset = pygame.image.load("Assets/apple.png")
        self.snake = Snake(size)
        self.surface = None

    def empty_arena(self):
        self.surface.fill(self.DEFAULT_BCKG)

        pygame.draw.rect(self.surface, self.BDR_COLOR, 
            [0, 0, self.surface.get_width(), 1])
        pygame.draw.rect(self.surface, self.BDR_COLOR, 
            [0, self.surface.get_height()-1, self.surface.get_width(), 1])
        pygame.draw.rect(self.surface, self.BDR_COLOR, 
            [0, 0, 1, self.surface.get_height()])
        pygame.draw.rect(self.surface, self.BDR_COLOR, 
            [self.surface.get_width()-1, 0, 1, self.surface.get_height()])

    def link_parent(self, subsurface):
        self.surface = subsurface
        self.display_arena()

    def generate_apple(self):
        self.apple_pos = -1

        valid_pos = []
        for i in range(self.size**2):
            if i != self.apple_pos and not (i in self.snake.snake_pos):
                valid_pos.append(i)

        if len(valid_pos) != 0:
            self.apple_pos = valid_pos[random.randrange(len(valid_pos))]

    def has_get_apple(self):
        return self.snake.snake_pos[0] == self.apple_pos

    def has_lose(self):
        head_pos = self.snake.snake_pos[0]
        head_ori = self.snake.head_orientation
        # Head bite snake
        if head_pos in self.snake.snake_pos[1:]:
            return True

        # Hit top or botton wall
        if head_pos < 0 or head_pos >= self.size**2:
            return True

        # Hit left wall
        if head_pos % self.size == self.size-1 and head_ori == Snake.M_LEFT:
            return True

        # Hit right wall
        if head_pos % self.size == 0 and head_ori == Snake.M_RIGHT:
            return True

    def display_arena(self):
        self.empty_arena()

        # render apple
        self.surface.blit(self.apple_asset, 
            [self.BDR_SIZE + (self.apple_pos%self.size) * self.ASQR_SIZE,
             self.BDR_SIZE + (self.apple_pos//self.size) * self.ASQR_SIZE])

        # render snake
        for i in range(len(self.snake.snake_pos)):
            pos = self.snake.snake_pos[i]
            self.surface.blit(
                self.snake.asset,
                (self.BDR_SIZE + (pos%self.size) * self.ASQR_SIZE,
                 self.BDR_SIZE + (pos//self.size) * self.ASQR_SIZE),
                self.snake.get_asset_part(i)
                )

        self.snake.normal_ondulation = not(self.snake.normal_ondulation)

    def get_width(self):
        return self.size*self.ASQR_SIZE + self.BDR_SIZE*2

    def get_height(self):
        return self.size*self.ASQR_SIZE + self.BDR_SIZE*2

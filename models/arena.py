#!/usr/bin/python

__version__ = "1.1.0"
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

    def __init__(self, size, use_ai=False):
        self.size = max(size, 5)
        self.apple_pos = -1
        self.apple_asset = pygame.image.load("Assets/apple.png")
        self.snake = Snake(size, use_ai)
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

    def get_ai_input(self):
        result = [0] * 32

        apple_view_index = 8
        wall_view_index = apple_view_index + 8
        body_view_index = wall_view_index + 8

        result[self.snake.head_orientation] = 1
        result[self.snake.tail_orientation+4] = 1

        dist = 0
        direction_checked = 0
        head_pos = self.snake.snake_pos[0]

        while direction_checked != 255:
            dist += 1

            # Check up
            if not(direction_checked & 1):
                pos = head_pos - dist*self.size

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif pos < 0:
                    index = wall_view_index

                if index is not None:
                    result[index] = 1 / dist
                    direction_checked |= 1

            # Check upper right
            if not(direction_checked & 2):
                pos = head_pos - dist*(self.size - 1)

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif pos < 0 or (pos%self.size) == 0:
                    index = wall_view_index

                if index is not None:
                    result[index+1] = 1 / dist
                    direction_checked |= 2

            # Check right
            if not(direction_checked & 4):
                pos = head_pos - dist*-1

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif (pos%self.size) == 0:
                    index = wall_view_index

                if index is not None:
                    result[index+2] = 1 / dist
                    direction_checked |= 4

            # Check bottom right
            if not(direction_checked & 8):
                pos = head_pos - dist*(-self.size-1)

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif pos >= self.size**2 or (pos%self.size) == 0:
                    index = wall_view_index

                if index is not None:
                    result[index+3] = 1 / dist
                    direction_checked |= 8

            # Check down
            if not(direction_checked & 16):
                pos = head_pos - dist*-self.size

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif pos >= self.size**2:
                    index = wall_view_index

                if index is not None:
                    result[index+4] = 1 / dist
                    direction_checked |= 16

            # Check bottom left
            if not(direction_checked & 32):
                pos = head_pos - dist*(-self.size+1)

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif pos >= self.size**2 or (pos%self.size) == self.size-1:
                    index = wall_view_index

                if index is not None:
                    result[index+5] = 1 / dist
                    direction_checked |= 32

            # Check left
            if not(direction_checked & 64):
                pos = head_pos - dist

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif (pos%self.size) == self.size-1:
                    index = wall_view_index

                if index is not None:
                    result[index+6] = 1 / dist
                    direction_checked |= 64

            # Check upper left
            if not(direction_checked & 128):
                pos = head_pos - dist*(self.size+1)

                index = None
                if pos == self.apple_pos:
                    index = apple_view_index
                elif pos in self.snake.snake_pos:
                    index = body_view_index
                elif pos < 0 or (pos%self.size) == self.size-1:
                    index = wall_view_index

                if index is not None:
                    result[index+7] = 1 / dist
                    direction_checked |= 128

        return [result]
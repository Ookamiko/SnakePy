#!/usr/bin/python

__version__ = "1.0.0"
__author__ = "Valentin 'Ookamiko' Dewilde"

import pygame

class Snake:

    M_RIGHT = 1
    M_UP = 2
    M_LEFT = 3
    M_DOWN = 4

    ASSET_SIZE = 15

    def __init__(self, arena_size):
        self.arena_size = arena_size
        start_pos = arena_size // 2 * (arena_size+1)
        self.snake_pos = [pos for pos in range(start_pos, start_pos-3, -1)]
        self.move_modif = 0
        self.head_orientation = self.M_RIGHT
        self.tail_orientation = self.M_RIGHT
        self.asset = pygame.image.load("Assets/snake.png")
        self.normal_ondulation = True

    def increase(self, tail):
        self.snake_pos.append(tail)
        self.update_tail_orientation()

    def update_move_modif(self, new_modif):
        if (new_modif == self.M_LEFT
                and self.head_orientation != self.M_RIGHT):
            self.move_modif = -1
            self.head_orientation = self.M_LEFT
        elif (new_modif == self.M_UP
                and self.head_orientation != self.M_DOWN):
            self.move_modif = -1 * self.arena_size
            self.head_orientation = self.M_UP
        elif (new_modif == self.M_RIGHT
                and self.head_orientation != self.M_LEFT):
            self.move_modif = 1
            self.head_orientation = self.M_RIGHT
        elif (new_modif == self.M_DOWN
                and self.head_orientation != self.M_UP):
            self.move_modif = self.arena_size
            self.head_orientation = self.M_DOWN

    def move_snake(self):
        tail_pos = self.snake_pos[len(self.snake_pos)-1]

        if self.move_modif == 0:
            return tail_pos

        new_pos = [self.snake_pos[0] + self.move_modif]
        for i in range(len(self.snake_pos)-1):
            # noinspection PyUnresolvedReferences
            new_pos.append(self.snake_pos[i])

        self.snake_pos = new_pos

        self.update_tail_orientation()

        return tail_pos

    def update_tail_orientation(self):
        tail = self.snake_pos[len(self.snake_pos)-1]
        before_tail = self.snake_pos[len(self.snake_pos)-2]

        if tail - before_tail < 0:
            if tail - before_tail == -1:
                self.tail_orientation = self.M_RIGHT
            else:
                self.tail_orientation = self.M_DOWN
        else:
            if tail - before_tail == 1:
                self.tail_orientation = self.M_LEFT
            else:
                self.tail_orientation = self.M_UP

    def get_asset_part(self, indice):
        x = self.ASSET_SIZE
        y = self.ASSET_SIZE

        if indice == 0:
            # Head
            x *= 3
            y *= (self.head_orientation-1)
        elif indice == len(self.snake_pos)-1:
            # Tail
            x = 0
            y *= (self.tail_orientation-1)
        else:
            # Body
            part_pos = self.snake_pos[indice]
            ahead_pos = self.snake_pos[indice-1]
            behind_pos = self.snake_pos[indice+1]

            # Check if ahead and behind part are aline
            if (behind_pos%self.arena_size == ahead_pos%self.arena_size
                or behind_pos//self.arena_size == ahead_pos//self.arena_size):
                
                if self.normal_ondulation:
                    x *= (1 + indice%2)
                else:
                    x *= (2 - indice%2)

                # Check orientation
                if behind_pos-part_pos < 0:
                    if behind_pos-part_pos == -1:
                        y = 0
                    else:
                        y *= 3
                else:
                    if behind_pos-part_pos == 1:
                        y *= 2

            # Check if behind part is to the left of the ahead part
            elif behind_pos%self.arena_size < ahead_pos%self.arena_size:
                # Check orientation
                if behind_pos-part_pos == -1:
                    if ahead_pos-part_pos == self.arena_size:
                        x *= 4
                        y *= 3
                    else:
                        x *= 5
                        y *= 2
                else:
                    if behind_pos-part_pos == self.arena_size:
                        x *= 4
                        y = 0
                    else:
                        x *= 5
            else:
                # Check orientation
                if behind_pos-part_pos == 1:
                    if ahead_pos-part_pos == self.arena_size:
                        x *= 5
                        y = 0
                    else:
                        x *= 4
                else:
                    if behind_pos-part_pos == self.arena_size:
                        x *= 5
                        y *= 3
                    else:
                        x *= 4
                        y *= 2

        return [x, y, self.ASSET_SIZE, self.ASSET_SIZE]

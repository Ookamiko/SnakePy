#!/usr/bin/python

__version__ = "1.0.0"
__author__ = "Valentin 'Ookamiko' Dewilde"

class Snake:

    M_LEFT = 1
    M_UP = 2
    M_RIGHT = 4
    M_DOWN = 8

    def __init__(self, arena_size):
        self.arena_size = arena_size
        start_pos = arena_size // 2 * (arena_size+1)
        self.snake_pos = [start_pos, start_pos-1, start_pos-2]
        self.move_modif = 0
        self.head_orientation = self.M_RIGHT
        self.tail_orientation = self.M_RIGHT

    def increase(self, tail):
        self.snake_pos.append(tail)

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

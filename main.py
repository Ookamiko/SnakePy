#!/usr/bin/python

__version__ = "1.1.0"
__author__ = "Valentin 'Ookamiko' Dewilde"

import pygame
import sys
import os
import numpy as np

from models.board import Board
from jormungandr.population import Population
from jormungandr.organism import Organism

use_ai = "--useai" in sys.argv
file_stats = "stats.txt"
max_gen = 500
for arg in sys.argv:
    if "--file-stats=" in arg:
        file_stats = arg.replace("--file-stats=", "")
    if "--max-gen=" in arg:
        max_gen = int(arg.replace("--max-gen=", ""))


board_size = 50 if not(use_ai) else 10

board = Board("Snake Game - " + __version__, board_size, use_ai=use_ai)
clock = pygame.time.Clock()
game_over = False
finish = False

base_speed = 10
step = 0
framerate = 60 if not(use_ai) else 1024

if not(use_ai):
    while not finish:
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    finish = True
                else:
                    board.render_event(event)

            if step <= 0:
                game_over = board.next_step()
                if game_over:
                    board.display_game_over()
                step = framerate / (base_speed * (2 ** (board.hud.score//100)))
            else:
                step -= 1

            clock.tick(framerate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    finish = True
                elif event.key == pygame.K_r:
                    board.reset()
                    game_over = False

else:
    # AI game
    organisms = []
    for _ in range(500):
        organisms.append(Organism([32, 20, 12, 4]))

    snakes_ai = Population(organisms, max_generation=max_gen,
        mating_select="fitest_gaussian")

    while not finish:
        stats = {'apple': [], 'step': [], 'fitness': []}
        i = 0
        for snake in snakes_ai.individuals:
            game_over = False
            i += 1
            board.reset(generation=snakes_ai.current_gen, organism=i)

            while not game_over:

                # Force quit run
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_KP_PLUS:
                            framerate = framerate * 2
                        elif event.key == pygame.K_KP_MINUS:
                            framerate = np.ceil(framerate/2)

                snake_input = board.arena.get_ai_input()
                snake_output = snake.predict(np.array(snake_input))[0]
                movement = [x for x in np.argsort(snake_output)[::-1]][0]
                board.arena.snake.update_move_modif(movement)

                game_over = board.next_step()

                clock.tick(framerate)

            snake.fitness = board.get_fitness()
            stats['apple'].append(board.apple_take)
            stats['step'].append(board.move_made)
            stats['fitness'].append(snake.fitness)

        board.save_stats(stats, snakes_ai.current_gen, file=file_stats)
        snakes_ai.save_best_individual()
        finish = not(snakes_ai.next_generation())

pygame.quit()

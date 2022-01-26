#!/usr/bin/python

import pygame
from Models.board import Board

board = Board("Snake Game", 50)
clock = pygame.time.Clock()
game_over = False
finish = False

base_speed = 10
step = 0
framerate = 60

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
			step = framerate / (base_speed * (2 ** (board.hud.score // 100)))
		else:
			step -= 1

		clock.tick(framerate)

	if not(finish):
		board.display_game_over()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finish = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				finish = True
			elif event.key == pygame.K_r:
				board.reset()
				game_over = False

pygame.quit()
quit()
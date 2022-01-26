#!/usr/bin/python

import pygame
from Models.snake import Snake
from Models.hud import Hud
from Models.arena import Arena

class Board():

	HUD_HEIGHT = 50
	DEFAULT_BCKG = (0, 0, 0)
	FONT_COLOR = (255, 255, 255)

	def __init__(self, caption, arena_size):

		pygame.init()

		self.font = pygame.font.SysFont("times new roman", 20)

		self.arena = Arena(arena_size)
		self.window = pygame.display.set_mode((self.arena.get_width() + 20, self.arena.get_height() + 70))
		self.arena.link_parent(self.window.subsurface([10, self.HUD_HEIGHT + 10, self.arena.get_width(), self.arena.get_height()]))
		self.arena.generate_apple()
		self.arena.display_arena()

		self.hud = Hud()
		self.hud.link_parent(self.window.subsurface([0, 0, self.window.get_width(), self.HUD_HEIGHT]))

		pygame.display.update()
		pygame.display.set_caption(caption)

	def reset(self):
		self.window.fill(self.DEFAULT_BCKG)
		self.arena = Arena(self.arena.size)
		self.arena.link_parent(self.window.subsurface([10, self.HUD_HEIGHT + 10, self.arena.get_width(), self.arena.get_height()]))
		self.arena.generate_apple()
		self.arena.display_arena()

		self.hud = Hud()
		self.hud.link_parent(self.window.subsurface([0, 0, self.window.get_width(), self.HUD_HEIGHT]))

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

		# Check lose
		if self.arena.has_lose():
			self.arena.snake.snake_pos.pop(0)
			self.arena.display_arena()
			pygame.display.update()
			return True

		# Check apple
		if self.arena.has_get_apple():
			self.arena.snake.increase(tail_pos)
			self.arena.generate_apple()
			self.hud.increase_score(self.arena.APPLE_POINT)

		self.arena.display_arena()
		pygame.display.update()

		return False

	def display_game_over(self):
		game_over_1 = self.font.render("Your score: " + str(self.hud.score), False, self.FONT_COLOR)
		game_over_2 = self.font.render("You lose", False, self.FONT_COLOR)
		game_over_3 = self.font.render("Press R to restart or Q to exit", False, self.FONT_COLOR)
		self.window.blit(game_over_1, 
			[self.window.get_width() // 2 - game_over_1.get_width() // 2,
			self.window.get_height() // 2 - game_over_2.get_height() // 2 - game_over_1.get_height() - 10])
		self.window.blit(game_over_2, 
			[self.window.get_width() // 2 - game_over_2.get_width() // 2,
			self.window.get_height() // 2 - game_over_2.get_height() // 2])
		self.window.blit(game_over_3, 
			[self.window.get_width() // 2 - game_over_3.get_width() // 2,
			self.window.get_height() // 2 + game_over_2.get_height() // 2 + 10])
		pygame.display.update()
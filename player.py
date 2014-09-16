import pygame as game

class player(game.sprite.Sprite):
	image = None

	def __init__(self, location):
		game.sprite.Sprite.__init__(self)

		if player.image is None:
			player.image = game.image.load("images/playerfullhealth.png")

		self.image = player.image

		self.rect = self.image.get_rect()
		self.rect.topleft = location

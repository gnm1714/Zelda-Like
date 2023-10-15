import pygame, sys
from settings import *
from level import Level


class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.state = 'main_menu'
		self.level = Level()

		# sound
		self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
		self.main_sound.set_volume(0.01)
		self.main_sound.play(loops=-1)

		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 10)
		self.title_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 50)
		self.start_time = None


	def title_screen(self):
		self.screen.fill('#10FFAA')

		title_surf = self.title_font.render('Zelda Game', False, TEXT_COLOR)
		title_rect = title_surf.get_rect(
			midtop=(WIDTH // 2, HEIGHT // 2 - 150))
		self.screen.blit(title_surf, title_rect)

		start_surf = self.font.render('Press Z to Start', False, TEXT_COLOR)
		start_rect = start_surf.get_rect(
			midtop=(WIDTH // 2, HEIGHT // 2))
		self.screen.blit(start_surf, start_rect)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z:
					self.start_time = pygame.time.get_ticks()
					self.state = 'game'

		pygame.display.update()


	def play_game(self):
		current_time = pygame.time.get_ticks()

		if current_time - self.start_time >= 100:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == RESTART:
					self.main_sound.stop()
					main()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()


	def level_manager(self):
		if self.state == 'main_menu':
			self.title_screen()
		if self.state == 'game':
			self.play_game()


	def run(self):
		while True:
			self.level_manager()
			self.clock.tick(FPS)


def main():
	game = Game()
	game.run()


if __name__ == '__main__':
	main()
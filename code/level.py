import pygame
from magic import MagicPlayer
from settings import *
from support import *
from tile import Tile
from player import Player
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from pause import Pause
from death import Death


class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

		# ui
		self.ui = UI()
		self.pause = Pause(self.player)
		self.game_paused = False
		self.death = Death(self.player)
		self.game_over = False

		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

	# noinspection PyTypeChecker
	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('../graphics/grass'),
			'objects': import_folder('../graphics/objects')
		}

		for style, layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'grass':
							grass_surf = choice(graphics['grass'])
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', grass_surf)
						if style == 'object':
							object_surf = graphics['objects'][int(col)]
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_surf)
						if style == 'entities':
							if col == '394':
								self.player = Player(
									(x, y),
									[self.visible_sprites],
									self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic,
									self.destroy_magic
								)
							else:
								monster = ''
								if col == '390':
									monster = 'bamboo'
								elif col == '391':
									monster = 'spirit'
								elif col == '392':
									monster = 'raccoon'
								else:
									monster = 'squid'
								Enemy(monster, (x, y), [self.visible_sprites, self.attackable_sprites],
									  self.obstacle_sprites, self.damage_player, self.trigger_death_particles,
									  self.add_xp)


	# noinspection PyTypeChecker
	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])


	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None


	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center - pygame.math.Vector2(0, 50)
							group = self.visible_sprites

							for leaf in range(randint(3, 6)):
								self.animation_player.create_grass_particles(pos, [group])
								target_sprite.kill()
						else:
							target_sprite.get_damage(self.player, attack_sprite.sprite_type, )


	def damage_player(self, amount, attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()

			pos = self.player.rect.center
			group = self.visible_sprites
			self.animation_player.create_particles(attack_type, pos, [group])

		if self.player.health <= 0:
			self.toggle_death()


	def toggle_death(self):
		self.game_over = True


	def trigger_death_particles(self, pos, particle_type):
		self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])


	def add_xp(self, amount):
		self.player.exp +=  amount


	def create_magic(self, style, strength, cost):
		if style == 'heal':
			self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
		elif style == 'flame':
			self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])


	def destroy_magic(self):
		pass


	def toggle_menu(self):
		self.game_paused = not self.game_paused


	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.ui.display(self.player)

		if self.game_paused:
			self.pause.display()
		elif self.game_over:
			self.death.display()
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)


	def enemy_update(self, player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)

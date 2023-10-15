import pygame 
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
	def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, destroy_magic):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

		self.import_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15

		self.direction = pygame.math.Vector2()
		self.attacking = False
		self.attack_cooldown = 200
		self.attack_time = None
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.create_magic = create_magic
		self.destroy_magic = destroy_magic

		self.obstacle_sprites = obstacle_sprites

		self.weapon_index = get_weapon_index()
		self.weapon = list(weapon_data.keys())[get_weapon_index()]

		self.magic_index = get_magic_index()
		self.magic = list(magic_data.keys())[get_magic_index()]

		self.vulnerable = True
		self.hurt_time = None
		self.invulnerability_duration = 300

		self.stats = {
			'health': 100,
			'energy': 50,
			'attack': 10,
			'magic': 4,
			'speed': 6
		}
		self.max_stats = {
			'health': 300,
			'energy': 140,
			'attack': 20,
			'magic': 10,
			'speed': 10
		}
		self.upgrade_cost = {
			'health': 100,
			'energy': 100,
			'attack': 100,
			'magic': 100,
			'speed': 100
		}
		self.health = self.stats['health']
		self.energy = self.stats['energy']
		self.exp = 123
		self.speed = self.stats['speed']

		self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
		self.weapon_attack_sound.set_volume(0.2)


	def import_assets(self):
		path = '../graphics/player/'
		self.animations = {
			'up': [], 'down': [], 'left': [], 'right': [],
			'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
			'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
		}

		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = import_folder(full_path)


	def input(self):
		keys = pygame.key.get_pressed()

		# movement
		if not self.attacking:
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

		# attack
		if keys[pygame.K_z] and not self.attacking:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()
			self.create_attack()
			self.weapon_attack_sound.play()

		# magic
		if keys[pygame.K_x] and not self.attacking:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()

			style = list(magic_data.keys())[self.magic_index]
			strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
			cost = list(magic_data.values())[self.magic_index]['cost']
			self.create_magic(style, strength, cost)


	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack', '')


	def get_full_weapon_damage(self):
		base_damage = self.stats['attack']
		weapon_damage = weapon_data[self.weapon]['damage']

		return base_damage + weapon_damage


	def get_full_magic_damage(self):
		base_damage = self.stats['magic']
		spell_damage = magic_data[self.magic]['strength']

		return base_damage + spell_damage


	def get_value_by_index(self, index):
		return list(self.stats.values())[index]


	def get_cost_by_index(self, index):
		return list(self.upgrade_cost.values())[index]


	def energy_recovery(self):
		if self.energy < self.stats['energy']:
			self.energy += 0.01
		else:
			self.energy = self.stats['energy']


	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				self.attacking = False
				self.destroy_attack()

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True


	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)


	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.energy_recovery()
		self.move(self.stats['speed'])
		self.weapon = list(weapon_data.keys())[get_weapon_index()]

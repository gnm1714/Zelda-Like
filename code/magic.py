import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'flame': pygame.mixer.Sound('../audio/fire.wav')
        }


    def heal(self, player, strength, cost, group):
        if player.energy >= cost:
            self.sounds['heal'].play()
            if player.health + strength <= player.stats['health']:
                player.health += strength
            else:
                player.health = player.stats['health']
            player.energy -= cost

            self.animation_player.create_particles('aura', player.rect.center, group)
            self.animation_player.create_particles('heal', player.rect.center, group)


    def flame(self, player, cost, group):
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(TILESIZE // -2, TILESIZE // 2)
                    y = player.rect.centery + randint(TILESIZE // -2, TILESIZE // 2)

                    self.animation_player.create_particles('flame', (x, y), group)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(TILESIZE // -2, TILESIZE // 2)
                    y = player.rect.centery + offset_y + randint(TILESIZE // -2, TILESIZE // 2)

                    self.animation_player.create_particles('flame', (x, y), group)

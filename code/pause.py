import pygame
from settings import *
from ui import UI
from support import *

class Pause:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.box_size = self.display_surface.get_size()[0] * 0.1

        self.pause_surface = pygame.Surface((WIDTH, HEIGHT))
        self.pause_surface.set_alpha(128)
        self.pause_surface.fill('#000000')
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.menu_items = ['Weapon', 'Magic']
        self.ui = UI()

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.show_menu = False

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            #weapon = pygame.transform.scale(weapon, (self.box_size, self.box_size - 30))
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            #magic = pygame.transform.scale(magic, (self.box_size - 30, self.box_size - 30))
            self.magic_graphics.append(magic)


    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_DOWN]:
                if self.selection_index < len(self.menu_items) - 1:
                    self.selection_index += 1
                else:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP]:
                if self.selection_index >= 1:
                    self.selection_index -= 1
                else:
                    self.selection_index = len(self.menu_items) - 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_z]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.selection_index = 0
                self.show_menu = True

            if keys[pygame.K_x] and self.show_menu:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.show_menu = False


    def menu_input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT]:
                if self.selection_index < len(self.weapon_graphics) - 1:
                    self.selection_index += 1
                else:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                if self.selection_index >= 1:
                    self.selection_index -= 1
                else:
                    self.selection_index = len(self.weapon_graphics) - 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN]:
                if self.selection_index < len(self.weapon_graphics) - 2:
                    self.selection_index += 2
                elif self.selection_index == len(self.weapon_graphics) - 2:
                    self.selection_index += 1
                else:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP]:
                if self.selection_index >= 2:
                    self.selection_index -= 2
                elif self.selection_index == 1:
                    self.selection_index = 0
                else:
                    self.selection_index = len(self.weapon_graphics) - 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_z]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.trigger(list(weapon_data.keys())[self.selection_index])
                self.selection_index = 0
                self.show_menu = False

            if keys[pygame.K_x]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.selection_index = 0
                self.show_menu = False


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()

            if current_time - self.selection_time >= 200:
                self.can_move = True


    def selection_box(self, left, top, text):
        bg_rect = pygame.Rect(left, top, self.box_size, self.box_size)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        if not self.show_menu:
            if text == self.menu_items[self.selection_index]:
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
            else:
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        else:
            border_rect = pygame.Rect(left - 2, top - 2, self.box_size + 4, self.box_size + 4)
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, border_rect)
            if text == list(weapon_data.keys())[self.selection_index]:
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, border_rect, 3)
            else:
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect


    def weapon_overlay(self, weapon_index, rect):
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)


    def magic_overlay(self, magic_index, rect):
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=rect.center)

        self.display_surface.blit(magic_surf, magic_rect)


    def trigger(self, name):
        if name in list(weapon_data.keys()):
            set_weapon_index(self.selection_index)
            self.selection_index = 0
        else:
            self.menu_input()


    def display(self):
        if not self.show_menu:
            self.input()
            self.selection_cooldown()

        self.display_surface.blit(self.pause_surface, (0, 0))

        self.ui.show_bar(self.player.health, self.player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.ui.show_bar(self.player.energy, self.player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        at_rect = self.selection_box(self.display_surface.get_size()[1] * 0.4,
                                     self.display_surface.get_size()[1] * 0.2, 'Weapon')  # weapon
        self.weapon_overlay(get_weapon_index(), at_rect)

        mg_rect = self.selection_box(self.display_surface.get_size()[1] * 0.4,
                                     self.display_surface.get_size()[1] * 0.5, 'Magic')  # magic
        self.magic_overlay(get_magic_index(), mg_rect)

        if self.show_menu:
            self.menu_input()
            self.selection_cooldown()

            # make background
            bg_rect = pygame.Surface((int(self.display_surface.get_size()[0] * 0.3),
                                      int(self.display_surface.get_size()[1] * 0.9)))
            bg_rect.set_alpha(192)
            bg_rect.fill((34, 34, 34))
            self.display_surface.blit(bg_rect, (self.display_surface.get_size()[0] // 2,
                                                int(self.display_surface.get_size()[1] * 0.05)))

            # fill w/ boxes
            for index in range(0, len(weapon_data)):
                left1 = (self.display_surface.get_size()[0] // 2) + int((self.display_surface.get_size()[0] * 0.3) // 7)
                left2 = (self.display_surface.get_size()[0] // 2) + int((self.display_surface.get_size()[0] * 0.3) // 1.85)
                top = int(self.display_surface.get_size()[1] * 0.05) + 20
                if index % 2 == 0:
                    box = self.selection_box(left1, top + ((self.box_size // 1.15) * index), list(weapon_data.keys())[index])
                    pygame.draw.rect(self.display_surface, UI_BG_COLOR, box)
                    self.weapon_overlay(index, box)
                else:
                    box = self.selection_box(left2, top + ((self.box_size // 1.15) * (index - 1)), list(weapon_data.keys())[index])
                    pygame.draw.rect(self.display_surface, UI_BG_COLOR, box)
                    self.weapon_overlay(index, box)



class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font


    def display_names(self, surface, name, cost, selected):
        color = 'gold' if selected else TEXT_COLOR

        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))

        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)


    def display_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = 'gold' if selected else 'white'

        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        pygame.draw.line(surface, color, top, bottom)
        pygame.draw.rect(surface, color, value_rect)


    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]


    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, 'gold', self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)

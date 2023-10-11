import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)


    def show_bar(self, current, max_amt, bg, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg)

        ratio = current / max_amt
        current_width = bg.width * ratio
        current_rect = bg.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg, 3)


    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright = (self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] - 20))

        self.display_surface.blit(text_surf, text_rect)


    def selection_box(self, left, top, text, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        text_surf = self.font.render(text, False, TEXT_COLOR)
        text_rect = text_surf.get_rect(midbottom=(left + (ITEM_BOX_SIZE / 2), top - 5))

        self.display_surface.blit(text_surf, text_rect)

        return bg_rect


    def weapon_overlay(self, weapon_index, rect):
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)


    def magic_overlay(self, magic_index, rect):
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=rect.center)

        self.display_surface.blit(magic_surf, magic_rect)


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)
        at_rect = self.selection_box(10, self.display_surface.get_size()[1] - (ITEM_BOX_SIZE + 10), 'Space', not player.can_switch_weapon) # weapon
        self.weapon_overlay(player.weapon_index, at_rect)

        mg_rect = self.selection_box(ITEM_BOX_SIZE + 20, self.display_surface.get_size()[1] - (ITEM_BOX_SIZE + 10), 'Shift', not player.can_switch_magic) # magic
        self.magic_overlay(player.magic_index, mg_rect)

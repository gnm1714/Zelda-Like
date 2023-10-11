import pygame, sys
from settings import *

class Death:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.height = 50
        self.width = 300
        self.create_items()

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        self.options = ['Restart', 'Quit']


    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_s] and self.selection_index < 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_w] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()

            if current_time - self.selection_time >= 200:
                self.can_move = True


    def create_items(self):
        self.item_list = []

        item = Item((self.display_surface.get_size()[0] // 2) - 150, (self.display_surface.get_size()[1] // 2), self.width, self.height, 0, self.font)
        self.item_list.append(item)
        item = Item((self.display_surface.get_size()[0] // 2) - 150, (self.display_surface.get_size()[1] // 2) + 75, self.width, self.height, 1, self.font)
        self.item_list.append(item)


    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.options[index]
            item.display(self.display_surface, self.selection_index, name)


class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font

        self.options = ['Restart', 'Quit']


    def display_names(self, surface, name, selected):
        color = 'gold' if selected else TEXT_COLOR

        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 15))

        surface.blit(title_surf, title_rect)


    def trigger(self, player):
        option = self.options[self.index]

        if option == 'Restart':
            pygame.event.post(pygame.event.Event(RESTART))
        elif option == 'Quit':
            pygame.quit()
            sys.exit()


    def display(self, surface, selection_num, name):
        if self.index == selection_num:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, 'gold', self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, self.index == selection_num)

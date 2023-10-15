import pygame
from settings import *

class Pause:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.pause_items = ['Equip', 'Items', 'Level Up', 'Stats', 'Save']
        self.pause_item = True
        self.pause_surface = pygame.Surface((WIDTH, HEIGHT))
        self.pause_surface.set_alpha(128)
        self.pause_surface.fill('#000000')

        self.height = self.display_surface.get_size()[1] * 0.4
        self.width = self.display_surface.get_size()[0] // 6
        self.create_pause_items()

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True


    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT]:
                if self.selection_index < self.attribute_number - 1:
                    self.selection_index += 1
                else:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                if self.selection_index >= 1:
                    self.selection_index -= 1
                else:
                    self.selection_index = self.attribute_number - 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_z]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                if self.pause_item:
                    self.pause_item = False
                    self.item_list[self.selection_index].trigger(self.player)
                else:
                    pass

            if keys[pygame.K_x]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                if not self.pause_item:
                    self.pause_item = True


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()

            if current_time - self.selection_time >= 200:
                self.can_move = True


    def create_pause_items(self):
        self.item_list = []
        self.inventory_items = []

        top = self.display_surface.get_size()[1] * 0.10
        left = self.display_surface.get_size()[0] * 0.3
        weapon = Item(left, top, self.width * 0.6, self.width * 0.6, 0, self.font, self.pause_item)
        self.inventory_items.append(weapon)

        top = self.display_surface.get_size()[1] * 0.35
        left = self.display_surface.get_size()[0] * 0.25
        magic1 = Item(left, top, self.width * 0.6, self.width * 0.6, 1, self.font, self.pause_item)
        self.inventory_items.append(magic1)

        left = self.display_surface.get_size()[0] * 0.35
        magic2 = Item(left, top, self.width * 0.6, self.width * 0.6, 2, self.font, self.pause_item)
        self.inventory_items.append(magic2)

        for item, index in enumerate(range(self.attribute_number)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2
            top = self.display_surface.get_size()[1] * 0.65

            item = Item(left, top, self.width, self.height, index, self.font, self.pause_item)
            self.item_list.append(item)


    def display(self):
        self.input()
        self.selection_cooldown()

        self.display_surface.blit(self.pause_surface, (0,0))

        for index, item in enumerate(self.item_list):
            name = self.pause_items[index]
            # value = self.player.get_value_by_index(index)
            # max_value = self.max_values[index]
            # cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name)

        for index, item in enumerate(self.inventory_items):
            item.display(self.display_surface, self.selection_index, "menu_Test")


class Item:
    def __init__(self, l, t, w, h, index, font, pause_item):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font

        self.pause_items = ['Equip', 'Items', 'Level Up', 'Stats', 'Save']
        self.pause_item = pause_item


    def display_names(self, surface, name, selected, cost=0):
        display_name = name
        if 'menu' in name:
            display_name = str(name.split('_')[1:]).strip('[]\',')
        if selected and 'menu' not in name:
            color = 'gold'
        else:
            color = TEXT_COLOR
        height = int(surface.get_size()[1] * 0.4)

        if cost > 0:
            title_surf = self.font.render(display_name, False, color)
            title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))
            surface.blit(title_surf, title_rect)

            cost_surf = self.font.render(f'{int(cost)}', False, color)
            cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))
            surface.blit(cost_surf, cost_rect)
        else:
            title_surf = self.font.render(display_name, False, color)
            title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, (height / 2) - 20))
            surface.blit(title_surf, title_rect)


    # def display_bar(self, surface, value, max_value, selected):
    #     top = self.rect.midtop + pygame.math.Vector2(0, 60)
    #     bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
    #     color = 'gold' if selected else 'white'
    #
    #     full_height = bottom[1] - top[1]
    #     relative_number = (value / max_value) * full_height
    #     value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)
    #
    #     pygame.draw.line(surface, color, top, bottom)
    #     pygame.draw.rect(surface, color, value_rect)


    def trigger(self, player):
        if self.pause_item and self.index == 0:
            self.pause_item = False
        else:
            selection = list(player.stats.keys())[self.index]



        # upgrade_attribute = list(player.stats.keys())[self.index]
        #
        # if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
        #     player.exp -= player.upgrade_cost[upgrade_attribute]
        #     player.stats[upgrade_attribute] *= 1.2
        #     player.upgrade_cost[upgrade_attribute] *= 1.4
        #
        # if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
        #     player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]


    def display(self, surface, selection_num, name, value = 0, max_value = 0, cost = 0):
        if self.index == selection_num and 'menu' not in name:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, 'gold', self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, self.index == selection_num, cost)
        #self.display_bar(surface, value, max_value, self.index == selection_num)

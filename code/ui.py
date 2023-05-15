import pygame
from settings import *


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        # BAR SETUP
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current / max_amount  # 95 / 100 = 0.95
        current_width = bg_rect.width * ratio  # new width
        current_rect = bg_rect.copy()  # copy for changing
        current_rect.width = current_width  # set new width for the copy

        pygame.draw.rect(self.display_surface, color, current_rect)  # color_of_bar
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)  # border

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20 # 1260
        y = self.display_surface.get_size()[1] - 20 # 700
        text_rect = text_surf.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)

    def show_heals(self, heals):
        text_surf = self.font.render(f'x{str(int(heals))}', False, TEXT_COLOR)
        x = 20
        y = self.display_surface.get_size()[1] - 20 # 70
        text_rect = text_surf.get_rect(bottomleft=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.show_heals(player.heals)
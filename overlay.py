import pygame
from settings import *


class Overlay:
    def __init__(self, player):

        self.display_surface = pygame.display.get_surface()  # Получаем поверхность для отображения
        self.player = player

        overlay_path = '../things/graphics/overlay/'
        # Загружаем изображения инструментов в словарь с ключами из инструментов игрока
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        # Загружаем изображения семян в словарь с ключами из семян игрока
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

    def display(self):

        # Отображение инструмента
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=overlay_positions['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # Отображение семян
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=overlay_positions['seed'])
        self.display_surface.blit(seed_surf, seed_rect)

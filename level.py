import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic


class Level:
    def __init__(self):
        # Получаем поверхность для отображения
        self.display_surface = pygame.display.get_surface()
        # Группы спрайтов
        self.all_sprites = CameraGroup()

        self.setup()  # Настройка уровня

        self.overlay = Overlay(self.player)  # Создаем оверлей для отображения информации

    def setup(self):
        # Добавление карты (фон)
        Generic(
            pos=(0, 0),
            surf=pygame.image.load('../things/graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=layers['ground']
        )

        # Добавление игрока
        center_x = screen_width // 2  # Центр по оси X
        center_y = screen_height // 2  # Центр по оси Y
        self.player = Player((center_x, center_y), self.all_sprites)  # Создаем игрока в центре экрана

    def run(self, dt):
        self.all_sprites.custom_draw(self.player)  # Рисуем все спрайты с учетом камеры
        self.all_sprites.update(dt)  # Обновляем все спрайты

        self.overlay.display()  # Отображаем оверлей


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # Получаем поверхность для отображения
        self.offset = pygame.math.Vector2()  # Смещение камеры

    def custom_draw(self, player):
        map_image = pygame.image.load('../things/graphics/ground.png').convert_alpha() # Загружаем карту
        map_width = map_image.get_width()
        map_height = map_image.get_height()

        self.offset.x = player.rect.centerx - screen_width // 2
        self.offset.y = player.rect.centery - screen_height // 2

        # Ограничение смещения камеры, чтобы не выйти за пределы карты
        self.offset.x = max(0, min(self.offset.x, map_width - screen_width))
        self.offset.y = max(0, min(self.offset.y, map_height - screen_height))

        # Отрисовка спрайтов с учётом сдвига камеры
        for layer in layers.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
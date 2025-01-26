import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic
import pytmx


class Level:
    def __init__(self):
        # Получаем поверхность для отображения
        self.display_surface = pygame.display.get_surface()
        # Группы спрайтов
        self.all_sprites = CameraGroup()

        self.setup()  # Настройка уровня

        self.overlay = Overlay(self.player)  # Создаем оверлей для отображения информации

    def setup(self):
        tmx_data = pytmx.util_pygame.load_pygame('./things/graphics/map.tmx')
        for layer in tmx_data.layers:
            print(layer.name)
        background_layer = tmx_data.get_layer_by_name("ground")
        # Добавление карты (фон)
        for x, y, gid in background_layer:
            tile_image = tmx_data.get_tile_image_by_gid(gid)
            if tile_image:  # Если тайл существует
                Generic(
                    pos=(x * tmx_data.tilewidth, y * tmx_data.tileheight),
                    surf=tile_image,
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
    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2()

            # Загрузка карты один раз
            self.map_image = pytmx.util_pygame.load_pygame('./things/graphics/map.tmx')

        def custom_draw(self, player):
            map_width = self.map_image.width * self.map_image.tilewidth
            map_height = self.map_image.height * self.map_image.tileheight

            self.offset.x = player.rect.centerx - screen_width // 2
            self.offset.y = player.rect.centery - screen_height // 2

            self.offset.x = max(0, min(self.offset.x, map_width - screen_width))
            self.offset.y = max(0, min(self.offset.y, map_height - screen_height))

            # Отрисовка спрайтов с учетом сдвига камеры
            for layer in layers.values():
                for sprite in self.sprites():
                    if sprite.z == layer:
                        offset_rect = sprite.rect.copy()
                        offset_rect.center -= self.offset
                        self.display_surface.blit(sprite.image, offset_rect)


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft=pos)

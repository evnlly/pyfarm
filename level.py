import pytmx
from settings import *
from player import Player
import pygame


class Level:
    def __init__(self):
        # Получаем поверхность экрана
        self.display_surface = pygame.display.get_surface()

        # Создаем группы спрайтов для управления объектами игры
        self.all_sprites = CameraGroup()  # Группа всех спрайтов (учитывает камеру)
        self.collision_sprites = pygame.sprite.Group()  # Группа объектов с коллизией
        self.tree_sprites = pygame.sprite.Group()  # Группа деревьев
        self.interaction_sprites = pygame.sprite.Group()  # Группа объектов взаимодействия

        # Настройка уровня
        self.setup()

        # Фоновая музыка
        self.music = pygame.mixer.Sound('./things/graphics/audio/music.mp3')
        self.music.play(loops=-1)  # Зацикливаем музыку

    def setup(self):
        # Загружаем карту из файла Tiled
        tmx_data = pytmx.util_pygame.load_pygame('./things/graphics/map.tmx')

        # Добавляем слои пола и нижней мебели дома
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * tile_size, y * tile_size), surf, self.all_sprites, layers['house bottom'])

        # Добавляем стены и верхнюю мебель, также включаем коллизии
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * tile_size, y * tile_size), surf, [self.all_sprites, self.collision_sprites])

        # Добавляем другие объекты на карте
        for x, y, surf in tmx_data.get_layer_by_name("stuff").tiles():
            Generic((x * tile_size, y * tile_size), surf, [self.all_sprites, self.collision_sprites],
                    layers['ground plant'])

        for x, y, surf in tmx_data.get_layer_by_name("ways").tiles():
            Generic((x * tile_size, y * tile_size), surf, self.all_sprites, layers['ground plant'])

        for x, y, surf in tmx_data.get_layer_by_name("Trees").tiles():
            Generic((x * tile_size, y * tile_size), surf, [self.all_sprites, self.collision_sprites], layers['tree'])

        # Создаем коллизионные тайлы
        for x, y, _ in tmx_data.get_layer_by_name("Collision").tiles():
            Tile((x * tile_size, y * tile_size), pygame.Surface((tile_size, tile_size)), self.all_sprites)

        # Добавляем игрока в игру
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites)

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

    def run(self, dt):
        # Очищаем экран перед отрисовкой
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)  # Отрисовываем все спрайты

        # Обновляем все спрайты
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()  # Смещение камеры
        self.map_image = pytmx.util_pygame.load_pygame('./things/graphics/map.tmx')

    def custom_draw(self, player):
        # Получаем размеры карты
        map_width = self.map_image.width * self.map_image.tilewidth
        map_height = self.map_image.height * self.map_image.tileheight

        # Рассчитываем смещение камеры относительно игрока
        self.offset.x = player.rect.centerx - screen_width // 2
        self.offset.y = player.rect.centery - screen_height // 2

        # Ограничиваем движение камеры границами карты
        self.offset.x = max(0, min(self.offset.x, map_width - screen_width))
        self.offset.y = max(0, min(self.offset.y, map_height - screen_height))

        # Рисуем объекты на экране с учетом слоев
        for layer in layers.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset  # Применяем смещение камеры
                    self.display_surface.blit(sprite.image, offset_rect)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=0):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-tile_size // 4, -tile_size // 2)  # Создаем хитбокс для коллизии
        self.z = z


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=layers['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z  # Определяем уровень отрисовки
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)  # Хитбокс

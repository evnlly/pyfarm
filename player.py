import pygame
from settings import *
from timer import Timer
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        self.import_assets()  # Импортируем анимации игрока
        self.status = 'down_idle'  # Начальный статус анимации
        self.frame_index = 0  # Индекс кадра анимации

        # Общие настройки
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = layers['main']

        # Атрибуты движения
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200  # Скорость передвижения

        # Коллизии
        self.hitbox = self.rect.copy().inflate((-126, -70))  # Создание хитбокса
        self.collision_sprites = collision_sprites  # Список объектов с коллизией

        # Таймеры
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
        }

        # Инструменты
        self.tools = ['hoe', 'axe']  # Доступные инструменты
        self.tool_index = 0  # Индекс текущего инструмента
        self.selected_tool = self.tools[self.tool_index]  # Выбранный инструмент

        # Семена
        self.seeds = ['corn', 'tomato']  # Доступные семена
        self.seed_index = 0  # Индекс текущего семени
        self.selected_seed = self.seeds[self.seed_index]  # Выбранное семя

        # Инвентарь
        self.item_inventory = {
            'wood': 20,
            'apple': 20,
            'corn': 20,
            'tomato': 20
        }
        self.seed_inventory = {
            'corn': 5,
            'tomato': 5
        }
        self.money = 200  # Начальное количество денег

    def use_tool(self):
        pass  # Логика использования инструмента

    def import_folder(self, path):
        """Импортирует изображения из папки и возвращает список поверхностей"""
        surface_list = []
        for folder_name, sub_folder, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list

    def get_target_pos(self):
        """Получает координаты цели в зависимости от направления игрока"""
        self.target_pos = self.rect.center + player_tool_offset[self.status.split('_')[0]]

    def use_seed(self):
        pass  # Логика использования семян

    def import_assets(self):
        """Импорт анимаций персонажа"""
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': []}

        for animation in self.animations.keys():
            full_path = '../things/graphics/character/' + animation
            self.animations[animation] = self.import_folder(full_path)

    def animate(self, dt):
        """Анимация движения игрока"""
        self.frame_index += 3 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        """Обрабатывает ввод пользователя"""
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
            # Движение
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE] and not self.timers['tool use'].active:
                self.music = pygame.mixer.Sound(f'./things/graphics/audio/{self.selected_tool}.mp3')
                self.music.play()
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # Переключение инструмента
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index = (self.tool_index + 1) % len(self.tools)
                self.selected_tool = self.tools[self.tool_index]

            # Использование семян
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # Переключение семян
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index = (self.seed_index + 1) % len(self.seeds)
                self.selected_seed = self.seeds[self.seed_index]

    def get_status(self):
        """Обновляет статус игрока в зависимости от действий"""
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def move(self, dt):
        # Двигаем хитбокс вместо прямоугольника
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        # Обновляем основную позицию игрока
        self.rect.center = self.hitbox.center

    def update(self, dt):
        """Обновление состояния игрока каждый кадр"""
        for timer in self.timers.values():  # Обновляем все таймеры
            timer.update()
        self.input()
        self.get_target_pos()
        self.get_status()
        self.move(dt)
        self.animate(dt)

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Вправо
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # Влево
                        self.hitbox.left = sprite.hitbox.right
                if direction == 'vertical':
                    if self.direction.y > 0:  # Вниз
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # Вверх
                        self.hitbox.top = sprite.hitbox.bottom



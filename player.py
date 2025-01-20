import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()  # Импортируем анимационные кадры
        self.status = 'down_idle'  # Начальный статус (стояние вниз)
        self.frame_index = 0  # Индекс текущего кадра анимации

        # Общие настройки
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = layers['main']

        # Атрибуты движения
        self.direction = pygame.math.Vector2()  # Направление движения
        self.pos = pygame.math.Vector2()  # Позиция игрока
        self.speed = 200  # Скорость движения

        # Таймеры для инструментов и смены семян
        self.timers = {
            'tool use': Timer(2000, self.use_tool),
            'tool switch': Timer(200),
            'seed switch': Timer(200),
            'seed use': Timer(2000, self.use_seed)
        }

        # Инструменты
        self.tools = ['hoe', 'axe', 'water']  # Доступные инструменты
        self.tool_index = 0  # Индекс выбранного инструмента
        self.selected_tool = self.tools[self.tool_index]  # Текущий выбранный инструмент

        # Семена
        self.seeds = ['corn', 'tomato']  # Доступные семена
        self.seed_index = 0  # Индекс выбранного семени
        self.selected_seed = self.seeds[self.seed_index]  # Текущее выбранное семя

    def use_tool(self):
        pass

    def use_seed(self):
        pass

    def import_assets(self):
        # Импортируем все анимации для разных состояний игрока
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        for animation in self.animations.keys():
            full_path = '../things/graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)  # Загружаем анимации

    def animate(self, dt):
        # Обновляем индекс кадра анимации
        self.frame_index += 4 * dt  # Увеличиваем индекс кадра с учетом времени
        if self.frame_index >= len(self.animations[self.status]):  # Если кадры закончились, начинаем сначала
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]  # Обновляем изображение персонажа

    def input(self):
        keys = pygame.key.get_pressed()  # Получаем состояние всех клавиш

        if not self.timers['tool use'].active:  # Если таймер использования инструмента не активен
            # Управление движением
            if keys[pygame.K_UP]:
                self.status = 'up'  # Статус движения вверх
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.status = 'down'  # Статус движения вниз
                self.direction.y = 1
            else:
                self.direction.y = 0  # Нет движения по вертикали

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1  # Статус движения вправо
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1  # Статус движения влево
                self.status = 'left'
            else:
                self.direction.x = 0  # Нет движения по горизонтали

            # Использование инструмента
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()  # Активируем таймер для использования инструмента
                self.direction = pygame.math.Vector2()  # Останавливаем движение
                self.frame_index = 0  # Сбрасываем анимацию

            # Смена инструмента
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()  # Активируем таймер для смены инструмента
                self.tool_index += 1  # Переходим к следующему инструменту
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0  # Окружная смена
                self.selected_tool = self.tools[self.tool_index]  # Обновляем выбранный инструмент

            # Использование семени
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()  # Активируем таймер для использования семени
                self.direction = pygame.math.Vector2()  # Останавливаем движение
                self.frame_index = 0  # Сбрасываем анимацию

            # Смена семени
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()  # Активируем таймер для смены семени
                self.seed_index += 1  # Переходим к следующему семени
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0  # Окружная смена
                self.selected_seed = self.seeds[self.seed_index]  # Обновляем выбранное семя

    def get_status(self):
        # Если игрок не двигается
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'  # Статус становится "idle" (стояние)

        # Если используется инструмент
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool  # Добавляем инструмент к статусу

    def update_timers(self):
        for timer in self.timers.values():  # Обновляем все таймеры
            timer.update()

    def move(self, dt):
        # Нормализуем вектор направления (чтобы движение было одинаковым по всем осям)
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Движение по горизонтали
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Движение по вертикали
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)

import pygame


class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True  # Активируем таймер
        self.start_time = pygame.time.get_ticks()  # Запоминаем текущее время

    def deactivate(self):
        self.active = False  # Деактивируем таймер
        self.start_time = 0  # Сбрасываем время старта

    def update(self):
        current_time = pygame.time.get_ticks()  # Получаем текущее время
        # Если прошло время больше или равно длительности таймера
        if current_time - self.start_time >= self.duration:
            self.deactivate()  # Деактивируем таймер
            if self.func:  # Если была передана функция, вызываем ее
                self.func()

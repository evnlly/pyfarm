import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=layers['main']):
        super().__init__(groups)  # Инициализация родительского класса Sprite и добавление объекта в группы
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

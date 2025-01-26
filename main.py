import pygame
import sys
from settings import *
from level import Level
import pytmx


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("pyfarm")  # Устанавливаем заголовок окна
        self.screen = pygame.display.set_mode((screen_width, screen_height))  # Устанавливаем размер окна игры
        self.clock = pygame.time.Clock()  # Создаем объект для управления частотой кадров
        self.level = Level()  # Создаем уровень игры

    def run(self):
        while True:
            for event in pygame.event.get():  # Обрабатываем все события
                if event.type == pygame.QUIT:  # Если событие - закрытие окна
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(60) / 1000  # Получаем время, прошедшее с последнего кадра (в секундах)
            self.level.run(dt)  # Обновляем и рисуем уровень
            pygame.display.update()  # Обновляем экран
        for layer in tmx_data.visible_layers:
            # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 128, y * 128)
                    Tile(pos=pos, surf=surf, groups=sprite_group)

        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.type in ('Building', 'Vegetation'):
                Tile(pos=pos, surf=obj.image, groups=sprite_group)


if __name__ == "__main__":
    game = Game()
    game.run()

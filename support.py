from os import walk
import pygame


def import_folder(path):
    surface_list = []  # Список для хранения изображений

    for folder_name, sub_folder, img_files in walk(path):  # Проходим по всем папкам и файлам в указанной директории
        for image in img_files:
            full_path = path + '/' + image  # Формируем полный путь к изображению
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list  # Возвращаем список с изображениями


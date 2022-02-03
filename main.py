import pygame
import sys
import os
import requests
import math


class MapParameters(object):
    def __init__(self):
        self.lat = 36.88  # Широта
        self.lon = 50.22  # Долгота
        self.zoom = 15  # Масштаб (изменяется в пределах от 1 до 19)
        self.type = "map"  # Тип карты
        self.step = 0.005  # Шаг смещения карты

    def get_ll(self):  # Функция возвращает координаты в правильном формате
        return str(self.lon) + "," + str(self.lat)

    def process_key(self, event):  # Функция, которая обрабатывает события клавиатуры
        # Обработка клавиш для изменения масштаба (классная работа, задача 2)
        if event.key == pygame.K_PAGEUP and self.zoom < 19:
            self.zoom += 1

        elif event.key == pygame.K_PAGEDOWN and self.zoom > 1:
            self.zoom -= 1

        # Обработка клавиш для перемещения центра карты (классная работа, задача 3)
        elif event.key == pygame.K_LEFT:
            self.lon -= self.step * math.pow(2, 15 - self.zoom)

        elif event.key == pygame.K_RIGHT:
            self.lon += self.step * math.pow(2, 15 - self.zoom)

        elif event.key == pygame.K_UP and self.lat < 85:
            self.lat += self.step * math.pow(2, 15 - self.zoom)

        elif event.key == pygame.K_DOWN and self.lat > -85:
            self.lat -= self.step * math.pow(2, 15 - self.zoom)


# Создание карты
def load_map(map_pars):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={map_pars.get_ll()}&z={map_pars.zoom}&l={map_pars.type}"
    response = requests.get(map_request)

    if not response:
        print("Ошибочка вышла! Неправильный запрос :(")
        print(map_request)
        sys.exit()

    # Запись полученной картинки в файл
    map_file = "map.png"

    try:
        with open(map_file, "wb") as file:
            file.write(response.content)

    except IOError as exc:
        print("Ошибочка вышла! Не удалось записать картинку в файл ;(:", exc)
        sys.exit()

    return map_file


def main():
    pygame.init()
    size = 600, 450
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Maps-API-task')

    # Инициализация параматров карты
    map_pars = MapParameters()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYUP:  # Если была нажата какая-либо клавиша, она обрабатывается методом класса
                map_pars.process_key(event)

        # Создание файла с картой
        map_file = load_map(map_pars)

        # Отрисовка картинки
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    # Удаление файла с картинкой (больше не нужна)
    os.remove(map_file)


if __name__ == "__main__":
    main()

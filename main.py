import pygame, requests, sys, os


class MapParams(object):
    def __init__(self):
        self.lat = 36.88
        self.lon = 50.22
        self.zoom = 15
        self.type = "map"

    def get_ll(self):
        return str(self.lon) + "," + str(self.lat)


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


    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    map_pars = MapParams()

    while True:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

        # Создание файла с картой
        map_file = load_map(map_pars)

        # Отрисовка картинки
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    # Удаоение файла с картинкой (больше не нужна)
    os.remove(map_file)


if __name__ == "__main__":
    main()
import os
import sys
import pygame
from pygame.locals import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        global  buildings
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type in buildings:
            pygame.mixer.init()
            pygame.mixer.music.load("music\звук стройки.mp3")
            pygame.mixer.music.play()


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.fillColors = {
            'normal': '#FFFFFF',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.color = self.fillColors['normal']
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurface.fill(self.color)

        self.textSurface = font.render(buttonText, True, (20, 20, 20))

        buttons.append(self)



def buttons_draw(bg, buttons):
    for button in buttons:
        button.buttonSurface.fill(button.color)
        button.buttonSurface.blit(button.textSurface, (10, 10))
        bg.blit(button.buttonSurface, (button.x, button.y))

    screen.blit(bg, (0, 0))

    pygame.display.update()



def load_image(name):
    fullname = os.path.join('pygame_data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def generate_level(level):
    global x2, y2, flag3
    new_player, x, y = None, None, None
    if flag == 0:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '*':
                    Tile('empty', x, y)
                elif level[y][x] == 'X':
                    Tile('wall', x, y)
                elif level[y][x] == '0':
                    Tile('lakes', x, y)
                elif level[y][x] == 'C':
                    Tile('city', x, y)
                elif level[y][x] == 'W':
                    Tile('swamp', x, y)
                elif level[y][x] == 'B':
                    Tile('bad_emty', x, y)
                elif level[y][x] == 'q':
                    Tile("fish_house", x, y)
                elif level[y][x] == 'w':
                    Tile("tree_house", x, y)
                elif level[y][x] == 'e':
                    Tile("house", x, y)
                elif level[y][x] == 'r':
                    Tile("church", x, y)
        # вернем игрока, а также размер поля в клетках
    return new_player, x, y

def myFunction():
    print('Button Pressed')


def load_level(filename):
    filename = "pygame_data" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r+') as mapFile:
        level_map = [line.strip() for line in mapFile]


    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('горы.png'),
    'empty': load_image('grass.png'),
    'lakes': load_image('озеро.png'),
    'swamp': load_image('болото.png'),
    'city': load_image('замок.png'),
    'bad_emty': load_image('неплодородная_земля.png'),
    'fish_house': load_image('рыбацкий дом2.png'),
    'tree_house': load_image('лесопилка2.png'),
    'house': load_image('дом2.png'),
    'church': load_image('церковь2.png')
}

tile_width = tile_height = 50

buildings = ['church', 'house', 'tree_house', 'fish_house']

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flag = 0
flag_button = 0
flag2 = 0

if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load("music\фон.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.init()
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.SysFont('Arial', 40)

    buttons = []

    button1 = Button(410, 730, 165, 50, 'Уровень 1', myFunction)
    button2 = Button(410, 650, 165, 50, 'Уровень 2', myFunction)
    button3 = Button(410, 570, 165, 50, 'Уровень 3', myFunction)
    fon = pygame.transform.scale(load_image('fon_game.png'), (600, 800))
    buttons_draw(fon, buttons)
    pygame.mixer.music.play(-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and flag == 0:
                pos = pygame.mouse.get_pos()
                if (pos[0] >= 410 and pos[0] <= 575) and (pos[1] >= 730 and pos[1] <= 780):
                    player, level_x, level_y = generate_level(load_level('\level_1'))
                    screen.fill("black")
                    tiles_group.draw(screen)
                    flag = 1
                    flag2 = 1
                elif (pos[0] >= 410 and pos[0] <= 575) and (pos[1] >= 650 and pos[1] <= 700):
                    player, level_x, level_y = generate_level(load_level('\second_level.txt'))
                    screen.fill("black")
                    tiles_group.draw(screen)
                    flag = 1
                    flag2 = 2
                elif (pos[0] >= 410 and pos[0] <= 575) and (pos[1] >= 570 and pos[1] <= 620):
                    player, level_x, level_y = generate_level(load_level('\level_three.txt'))
                    screen.fill("black")
                    tiles_group.draw(screen)
                    flag = 1
                    flag2 = 3
            if flag_button != 0 and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x2, y2 = pos
                x2, y2 = (x2 - 0) // 50, (y2 - 0) // 50
                if flag_button == 1:
                    Tile("fish_house", x2, y2)
                if flag_button == 1:
                    Tile("tree_house", x2, y2)
                if flag_button == 2:
                    Tile("fish_house", x2, y2)
                if flag_button == 3:
                    Tile("house", x2, y2)
                if flag_button == 4:
                    Tile("church", x2, y2)
                flag_button = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    flag_button = 1
                elif event.key == pygame.K_w:
                    flag_button = 2
                elif event.key == pygame.K_e:
                    flag_button = 3
                elif event.key == pygame.K_r:
                    flag_button = 4

        pygame.display.flip()
        clock.tick(60)
        all_sprites.draw(screen)
        all_sprites.update()
    pygame.quit()
#модуль для объектов и повсеместно использующихся функций
import os
import sys
import pygame

def load_image(name, colorkey=None):
    '''Функция выгрузки изображений'''
    fullname = os.path.join(os.path.abspath('pygame_data3\images'), name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if not colorkey is None:
        image.set_colorkey(colorkey)
    return image

def draw_text(surf, text, font_name, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    return text_surface

class Tile(pygame.sprite.Sprite):
    tile_width = tile_height = 50 #размеры клетки

    def __init__(self, type, image, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.type = type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.rect = self.image.get_rect().move(Tile.tile_width * pos_x, Tile.tile_height * pos_y)

    def intersection(self, pos):
        '''метод позволяющий проверить находится ли данная точка на поверхности кнопки'''
        return self.rect.x <= pos[0] <= self.rect.x + self.rect.width and self.rect.y <= pos[1] <= self.rect.y + \
               self.rect.height

    def update(self, pos, new_img):
        global vol
        '''метод, обрабатывающий взаимодействие игрока со спрайтом'''
        pygame.init()
        s = pygame.mixer.Sound("musik\звук-стройки.wav")
        s.set_volume(0.1)
        if self.intersection(pos):
            if self.type == 'grass':
                self.image = pygame.transform.scale(load_image(new_img), (Tile.tile_width, Tile.tile_height))
                self.rect = self.image.get_rect().move(Tile.tile_width * self.pos_x, Tile.tile_height * self.pos_y)
                self.type = new_img[:-4]
                s.play()
                pygame.mixer.music.play()
            elif new_img == 'grass.png':
                self.image = pygame.transform.scale(load_image(new_img), (Tile.tile_width, Tile.tile_height))
                self.rect = self.image.get_rect().move(Tile.tile_width * self.pos_x, Tile.tile_height * self.pos_y)
                self.type = 'grass'


class Board:
    score_scheme = {'house': {'house': 5, 'castle': 5, 'church': 5, 'fisherman': -10, 'mount': -10},
                    'church': {'house': 5, 'castle': -30, 'fisherman': -10, 'water': -10, 'mount': -10},
                    'fisherman': {'water': 5, 'house': -10, 'castle': -10, 'church': -10, 'mount': -10,
                                  'fisherman': -5, 'swamp': -5},
                    'castle': {'house': 5, 'church': -30, 'fisherman': -10}}

    def __init__(self):
        self.width = 12
        self.height = 16
        self.board = [[None] * self.width for i in range(self.height)]

    def append(self, tile, row, col):
        self.board[row][col] = tile

    def intersection(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def score(self, row, col):
        score = 0
        neighborhood = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for neighbor in neighborhood:
            if self.intersection(row + neighbor[0], col + neighbor[1]):
                try:
                    score += Board.score_scheme[self.board[row][col].type][self.board[row + neighbor[0]][col + neighbor[1]].type]
                except Exception:
                    pass
        return score

    def all_score(self):
        score = 0
        for row in range(self.height):
            for col in range(self.width):
                score += self.score(row, col)
        return score




class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, onclickFunction, *group, buttonText='', font=None,
                 colors=('#FFFFFF', '#666666', '#333333'), width=50, height=50, image=None, **kwargs):
        super().__init__(*group)
        self.kwargs = kwargs

        #функция нажатия
        self.onclickFunction = onclickFunction

        #хитбокс кнопки
        if image is None:
            # цвета кнопки
            self.fillColors = {
                'normal': colors[0],
                'hover': colors[1],
                'pressed': colors[2],
            }
            self.color = self.fillColors['normal']

            self.image = pygame.Surface((self.width, self.height))
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.image.fill(self.color)
            self.textSurface = font.render(buttonText, True, (20, 20, 20))
        else:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def intersection(self, pos):
        '''метод позволяющий проверить находится ли данная точка на поверхности кнопки'''
        return self.rect.x <= pos[0] <= self.rect.x + self.rect.width and self.rect.y <= pos[1] <= self.rect.y + \
               self.rect.height

    def update(self, pos):
        '''обработка клика'''
        if self.intersection(pos):
            self.onclickFunction(self.kwargs['level'] if 'level' in self.kwargs else None)

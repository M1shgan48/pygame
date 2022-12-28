import os
import sys
import pygame
from pygame.locals import *


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


def load_image(name, colorkey=None):
    fullname = os.path.join('C:\pythonProject3\pygame_data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def myFunction():
    print('Button Pressed')

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont('Arial', 40)

    buttons = []

    fon = pygame.transform.scale(load_image('fon_game.jpg'), (width, height))

    button1 = Button(30, 30, 400, 100, 'Button One (onePress)', myFunction)
    button2 = Button(30, 140, 400, 100, 'Button Two (multiPress)', myFunction)

    buttons_draw(fon, buttons)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                pass
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

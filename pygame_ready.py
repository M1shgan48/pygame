import os
import pygame
import objects

class Display:
    def terminate(self):
        '''Метод удаляющий все спрайты'''
        for sprite in self.all_sprites:
            sprite.kill()

    def level_select_button_func(self, *args):
        '''Функция для кнопки перехода на экран выбора уровня'''
        self.terminate()
        self.level_select_render()

    def exit_button_func(self, *args):
        '''Функция кнопки выхода из игры'''
        pygame.quit()
        exit(0)

    def back_button_func(self, *args):
        '''Функция кнопки возврата в главное меню'''
        self.terminate()
        self.menu_render()

    def level_button_func(self, *args):
        '''Функция кнопки выбора уровня'''
        self.terminate()
        self.level_render(args[0])

    def menu_render(self):
        '''Метод отображающий главное меню на экране'''
        size = width, height = 800, 600
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.transform.scale(objects.load_image('fon_game.jpg'), size)
        self.score = 1e9

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()

        self.board = objects.Board()

        objects.Button(700, 50, self.exit_button_func, self.all_sprites, self.buttons,
                                     image=pygame.transform.scale(objects.load_image('exit_button.png'), (50, 50)))
        objects.Button(350, 250, self.level_select_button_func, self.all_sprites, self.buttons,
                                     image=pygame.transform.scale(objects.load_image('start_button.png'), (100, 100)))
        objects.Button(650, 530, self.musi_turn_off, self.all_sprites, self.buttons,
                                        image=pygame.transform.scale(objects.load_image('speaker.png'), (50, 50)))
        objects.Button(600, 530, self.switch_to_left, self.all_sprites, self.buttons,
                                     image=pygame.transform.scale(objects.load_image('switch_to_left.png'), (50, 50)))
        objects.Button(700, 530, self.switch_to_right, self.all_sprites, self.buttons,
                                      image=pygame.transform.scale(objects.load_image('switch_to_right.png'), (50, 50)))

        self.buttons.draw(self.background)
        self.screen.blit(self.background, (0, 0))

    def level_select_render(self):
        global flag_q, flag_r, flag_w
        flag_q, flag_r, flag_w = 0, 0, 0
        '''Метод отображающий меню выбора уровня'''
        size = width, height = 800, 600
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.transform.scale(objects.load_image('fon_game.jpg'), size)

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()

        objects.Button(50, 50, self.back_button_func, self.all_sprites, self.buttons,
                                     image=pygame.transform.scale(objects.load_image('back_button.png'), (150, 50)))
        objects.Button(150, 250, self.level_button_func, self.all_sprites, self.buttons,
                                          image=pygame.transform.scale(objects.load_image('start_button.png'), (50, 50)),
                                          level='first_level.txt')
        objects.Button(350, 250, self.level_button_func, self.all_sprites, self.buttons,
                                          image=pygame.transform.scale(objects.load_image('start_button.png'), (50, 50)),
                                          level='second_level.txt')
        objects.Button(550, 250, self.level_button_func, self.all_sprites, self.buttons,
                                          image=pygame.transform.scale(objects.load_image('start_button.png'), (50, 50)),
                                          level='level_three.txt')


        self.buttons.draw(self.background)
        self.screen.blit(self.background, (0, 0))

    def level_render(self, sample):
        with open(os.path.abspath(f'pygame_data3\levels/{sample}'), 'r') as scheme:
            self.scheme = scheme.read().split()

        size = width, height = 800, 800
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 150, 0))

        self.score = 85

        self.board = objects.Board()
        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()

        objects.Button(601, 725, self.back_button_func, self.all_sprites, self.buttons,
                                     image=pygame.transform.scale(objects.load_image('back_button.png'), (199, 50)))

        images = {'*': 'grass.png',
                  'X': 'mount2.png',
                  '0': 'water.png',
                  'C': 'castle.png',
                  'B': 'mount.jpg',
                  'W': 'swamp.png'}
        types = {'grass.png': 'grass',
                 'water.png': 'water',
                 'mount2.png': 'mount',
                 'castle.png': 'castle',
                 'swamp.png': 'swamp'}

        for row in range(len(self.scheme)):
            for col in range(len(self.scheme[row])):
                if images[self.scheme[row][col]] not in types:
                    type = 'NA'
                else:
                    type = types[images[self.scheme[row][col]]]
                tile = objects.Tile(type, pygame.transform.scale(objects.load_image(images[self.scheme[row][col]]), (50, 50)),
                                    col, row, self.all_sprites, self.tiles)
                self.board.append(tile, row, col)



    def win_screen_render(self):
        global score
        size = width, height = 800, 600
        self.screen = pygame.display.set_mode(size)

        self.screen.fill((255, 255, 255))

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        objects.Button(50, 50, self.back_button_func, self.all_sprites, self.buttons,
                                     image=pygame.transform.scale(objects.load_image('back_button.png'), (150, 50)))

        objects.draw_text(self.screen, 'YOU WON!', pygame.font.match_font('arial'), 100, 350, 250, (0, 0, 0))

        self.all_sprites.draw(self.screen)
        score = 0


    def switch_to_left(self, *args):
        '''Переключение музыки'''
        try:
            global music, vol
            music.append(music[0])
            del music[0]
            pygame.mixer.music.load(f'musik\{music[0]}')
            pygame.mixer.music.set_volume(vol)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def switch_to_right(self, *args):
        '''Переключение музыки'''
        try:
            global music, vol
            music.insert(0, music[-1])
            del music[-1]
            pygame.mixer.music.load(f'musik\{music[0]}')
            pygame.mixer.music.set_volume(vol)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def musi_turn_off(self, *args):
        try:
            '''Вкл/выкл музыки'''
            global flag_misic
            if flag_misic:
                pygame.mixer.music.unpause()
                flag_misic = False
            else:
                pygame.mixer.music.pause()
                flag_misic = True
        except Exception:
            pass


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load("musik\music_фон.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.init()
    current_display = Display()
    current_display.menu_render()
    font_name = pygame.font.match_font('arial')
    running = True
    surf = None
    score = 0
    flag_q, flag_w, flag_r = 0, 0, 0

    controls = {pygame.K_q: 'house.png',
                pygame.K_w: 'fisherman.png',
                pygame.K_e: 'church.png'}
    vol = 0.2
    flag_misic = False
    music = ['music_фон.mp3', 'фон2.mp3', 'фон3.mp3', 'фон4.mp3', 'фон5.mp3', 'фон6.mp3', 'фон7.mp3', 'фон8.mp3',
             'фон9.mp3', 'фон10.mp3']
    pygame.mixer.music.play(-1)
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                current_display.buttons.update(event.pos)
            if event.type == pygame.KEYDOWN:
                try:
                    if controls[event.key] == "house.png" and flag_q != 3:
                        flag_q += 1
                        current_display.tiles.update(pygame.mouse.get_pos(), controls[event.key])
                    if controls[event.key] == "fisherman.png" and flag_w != 3:
                        flag_w += 1
                        current_display.tiles.update(pygame.mouse.get_pos(), controls[event.key])
                    if controls[event.key] == "church.png" and flag_r != 1:
                        flag_r += 1
                        current_display.tiles.update(pygame.mouse.get_pos(), controls[event.key])
                except Exception:
                    pass
                pygame.draw.rect(current_display.screen, (0, 150, 0), (600, 0, 200, 50))
                score = current_display.board.all_score()
                objects.draw_text(current_display.screen, str(score), font_name, 50, 650, 0, (255, 255, 255))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                vol += 0.1
                pygame.mixer.music.set_volume(vol)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                vol -= 0.1
                pygame.mixer.music.set_volume(vol)
        if score >= current_display.score:
            current_display.terminate()
            current_display.win_screen_render()
        current_display.all_sprites.draw(current_display.screen)
    pygame.quit()
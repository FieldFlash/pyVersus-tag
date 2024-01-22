# pygame game GUI 0.1.0

import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

background = pygame.image.load('menuimg.png')
background = pygame.transform.scale(background, (1920, 1080))
background = background.convert()


manager = pygame_gui.UIManager((1920, 1080), 'theme.json')

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((840, 1080/2), (250, 150)),
                                             text='PLAY',
                                             manager=manager, object_id=ObjectID(class_id='@menu_buttons',
                                           object_id='#play_button'))

settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((840, 700), (250, 150)),
                                             text='SETTINGS',
                                             manager=manager, object_id=ObjectID(class_id='@menu_buttons',
                                           object_id='#settings_button'))

quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((840, 860), (250, 150)),
                                             text='QUIT',
                                             manager=manager, object_id=ObjectID(class_id='@menu_buttons',
                                           object_id='#quit_button'))


clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type ==  pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                pass
            if event.ui_element == settings_button:
                pass
            if event.ui_element == quit_button:
                is_running = False
                pygame.quit()

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

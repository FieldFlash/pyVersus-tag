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


clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

            
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

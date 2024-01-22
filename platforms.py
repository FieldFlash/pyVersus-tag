import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect_y = y
        self.color = color
        self.top = self.rect.y
        self.bottom = self.rect.bottom

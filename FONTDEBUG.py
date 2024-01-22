import pygame
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
text = font.render("Hello, Pygame!", True, (0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((255, 255, 255))
    screen.blit(text, (200, 200))
    pygame.display.flip()
    clock.tick(60)

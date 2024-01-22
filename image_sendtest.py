import pygame
from pickle import loads, dumps
pygame.init()
 
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("image tobytes")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 255))

class Face():
    def __init__(self, image, x ,y):
        self.image = pygame.image.load(image)
        self.image = self.image.convert()
        self.x = x
        self.y = y

face = Face("player.png", 290, 190)

faceinbytes = pygame.image.tobytes(face, "RGB")
print(faceinbytes)
faceinbytes = dumps(faceinbytes)
print(faceinbytes)     
faceinbytes = loads(faceinbytes)
clock = pygame.time.Clock()
keepGoing = True

# L - Loop
while keepGoing:

    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
    
    screen.blit(background, (0, 0))
    screen.blit(pygame.image.frombytes(faceinbytes,(50, 50), "RGB"), (290, 190))
    pygame.display.flip()
    
pygame.quit()    

        

import pygame

class Player():
    '''Player sprite that controls player movement and size'''
    def __init__(self, x, y, width, height, isIt):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,width,height)
        self.color = (255, 0, 0)
        self.width = width
        self.height = height
        self.vel = 7
        self.y_vel = 0
        self.gravity = 0.3
        self.canJump = False
        self.isIt = isIt
        self.lives = 3

    def draw(self, win):
        '''Renders the player on the screen'''
        pygame.draw.rect(win, self.color, self.rect)

    def getX(self):
        '''Getter that returns player's x value'''
        return self.x

    def getY(self):
        '''Getter that returns player's y value'''
        return self.y
    
    def getIt(self):
        '''Getter that returns player's isIt value'''
        return self.isIt

    def move(self):
        '''Controls the player's movement, velocity and gravity and the jumping'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_d]:
            self.x += self.vel
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        if self.canJump == True:
            if keys[pygame.K_SPACE]:
                self.y_vel = -8.6
                self.canJump = False
        if self.y_vel == 0:
            self.canJump = True
        # Calling update
        self.update()

    def update(self):
        '''Re-renders the player object with update attributes'''
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.y_vel += self.gravity
        self.y += self.y_vel
    
    def setLives(self, newLives):
        '''Sets the players life count'''
        self.lives = newLives

    def getLives(self):
        '''Gets the player current life count'''
        return self.lives

class Platform(pygame.sprite.Sprite):
    '''Platform sprite that renders physical platforms in the window'''
    def __init__(self, x, y, width, height, image, platform_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = platform_type

    def draw(self, win):
        '''Render the platform'''
        win.blit(self.image, self.rect.topleft)

class PlayerMask(pygame.sprite.Sprite):
    '''Mask sprite to overlay an image onto your player client side'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, win):
        '''Render the image'''
        win.blit(self.image, self.rect.topleft)
    
    def setX(self, playerX):
        '''Setter to redefine the x value of the PlayerMask object'''
        self.rect.x = playerX
    
    def setY(self, playerY):
        '''Setter to redefine the y value of the PlayerMask object'''
        self.rect.y = playerY


class StatLabel(pygame.sprite.Sprite):
    '''An mutatable text Label Sprite subclass'''
    def __init__(self, message, x_y_center, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 50)
        self.text = message
        self.center = x_y_center
        self.color = color  
                 
    def draw(self, win):
        '''Render and center the label text on each Refresh.'''
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        win.blit(self.image, self.rect.topleft)


class TimerLabel(pygame.sprite.Sprite):
    '''A label that counts time'''
    def __init__(self, font, initial_seconds, center_position):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.seconds = initial_seconds
        self.center = center_position
        self.update()  # Initial rendering

    def update(self):
        '''updates the time'''
        self.image = self.font.render(str(self.seconds), True, (0, 0, 0))
        self.rect = self.image.get_rect(center=self.center)

    def draw(self, win):
        '''renders the timer'''
        win.blit(self.image, self.rect.topleft)


class LivesLabel(pygame.sprite.Sprite):
    '''An mutatable live counter label Sprite subclass'''
    def __init__(self, lives, x_y_center):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 50)
        self.center = x_y_center
        self.lives = lives
                 
    def draw(self, win, lives):
        '''Render and center the label text on each Refresh.'''
        self.image = self.font.render(str(self.lives), 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        win.blit(self.image, self.rect.topleft)

    def subtractLive(self):
        '''decreases the playerLife by 1'''
        self.lives -= 1

    def setLives(self, setLives):
        '''sets lives to whatever argument is passed in (integer)'''
        self.lives = setLives

    def getLives(self):
        return self.lives
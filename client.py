"""
Name: PyVersus Tag!
Date: Thursday January 18
Author: Liam Shelston
Description: This is a multiplayer tag game. Whoever is IT has 20 seconds to tag the other player. If the time runs out before they tag the 
other player, the IT player loses a life. If the player tags the other player before 20 seconds is up, the player who is NOT IT loses a life.
Whoever reaches zero lives first loses, and the other wins.
"""

# Import and initialize

# Importing pygame module for game dev
import pygame

# Importing freetype module to solve FreeType 2 initialization errors in pygame_gui
import pygame.freetype

# Importing the network file to control sending and receiving information
import network

# Importing the sprites file to give access to all various sprites classes
import sprites

# Importing the pygame_gui module for UI design
import pygame_gui

# Extra necessary imports under pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

# Importing tkinter for a fun end screen :)
import tkinter

# Intializing pygame, pygame.font and pygame.mixer
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Display

# Defining window with and height
width = 1920
height = 1080
# Creating a pygame display surface with the width and height passed as arguments
win = pygame.display.set_mode((width, height))
# Setting the caption for the client
pygame.display.set_caption("client.mpgame")


# Entities

# Loading the music files, setting the volume and playing menu music on loop
pygame.mixer.music.load("menumusic.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
goSound = pygame.mixer.Sound("go.wav")
goSound.set_volume(0.5)
coinSound = pygame.mixer.Sound("coin.wav")
coinSound.set_volume(0.3)
coinSound.play()

# Assigning
lives = 3
playerIsIt = False

# Defining the sprites in the code
# Defining the Mask(s) for the Player(s)
playerMasks = [sprites.PlayerMask(1640, 200), sprites.PlayerMask(120, 200)]
# Defining the custom font used in the buttons
custom_font = pygame.font.Font(None, 36)
# Background image
background = pygame.image.load("gameimg.png")
# Platform sprites
platform_main = sprites.Platform(120, 800, 1600, 50, "groundmain.png", "main")
platform_high_1 = sprites.Platform(400, 610, 370, 25, "groundhigh.png", "high")
platform_high_2 = sprites.Platform(1000, 610, 370, 25, "groundhigh.png", "high")
platform_high_3 = sprites.Platform(1300, 430, 370, 25, "groundhigh.png", "high")
platform_high_4 = sprites.Platform(200, 430, 370, 25, "groundhigh.png", "high")
# Label sprites
livesLabel = sprites.StatLabel("Lives: ", (90, 25), (200, 0, 20))
livesNumberLabel = sprites.LivesLabel(lives, (200, 25))
timeLabel = sprites.TimerLabel(pygame.font.SysFont("Arial", 50), 20, (width // 2, 30))
itLabel = sprites.StatLabel(3, (1710, 25), (200, 0, 20))
gameOverLabel = sprites.StatLabel("Game Over", (width/2, height/2), (255,255,255))

# Action
def mainMenu():
    """This function controls all functions and objects in the main menu of the games"""

    # Loads and scales the background for the menu
    background = pygame.image.load("menuimg.png")
    background = pygame.transform.scale(background, (1920, 1080))
    background = background.convert()

    # Defining the manager for pygame_gui as well as attaching a json stylesheet file
    manager = pygame_gui.UIManager((1920, 1080), "theme.json")

    # Defining the size and ids for all the buttons on the main menu

    # Play button
    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((840, 1080 / 2), (250, 150)),
        text="PLAY",
        manager=manager,
        object_id=ObjectID(class_id="@menu_buttons", object_id="#play_button"),
    )

    # Kill Server button
    server_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((840, 700), (250, 150)),
        text="KILL SERVER",
        manager=manager,
        object_id=ObjectID(class_id="@menu_buttons", object_id="#server_button"),
    )

    # Quit button
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((840, 860), (250, 150)),
        text="QUIT",
        manager=manager,
        object_id=ObjectID(class_id="@menu_buttons", object_id="#quit_button"),
    )

    # Defining the pygame Clock
    clock = pygame.time.Clock()
    menu_running = True
    # Menu loop
    while menu_running:
        # Timer
        time_delta = clock.tick(60) / 1000.0
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            # When a button is pressed, perform action
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    # Triggers the game start upon pressed the Play button
                    triggerGameStart()
                    menu_running = False
                    print("play button pressed")
                if event.ui_element == server_button:
                    # Kills the server when pressed
                    pass
                if event.ui_element == quit_button:
                    # Closes the client
                    menu_running = False
                    pygame.quit()

            # Update all manager objects based on the events
            manager.process_events(event)

        # Refresh
        manager.update(time_delta)
        # Render the background and all objects contorlled by the manager() onto the main menu
        win.blit(background, (0, 0))
        manager.draw_ui(win)
        pygame.display.update()


# Action
def playingScreen():
    """Function that controls processes involving playing the game"""
    # globalizes the lives variable so it can be used in all functions in the playingScreen()
    global lives
    # sets lives to 3 at the beginning of the game
    livesNumberLabel.setLives(lives)


    def redrawWindow(
        win,
        background,
        player,
        player2,
        platform_main,
        platform_high_1,
        platform_high_2,
        platform_high_3,
        platform_high_4,
        pmask,
        lives,
    ):
        """Refresh display and check collisions"""
        win.fill((255, 255, 255))
        checkCollisions(
            player,
            player2,
            platform_main,
            platform_high_1,
            platform_high_2,
            platform_high_3,
            platform_high_4,
            pmask,
            lives,
        )
        # Draw everything
        win.blit(background, (0, 0))
        platform_main.draw(win)
        platform_high_1.draw(win)
        platform_high_2.draw(win)
        platform_high_3.draw(win)
        platform_high_4.draw(win)
        player2.draw(win)
        playerMasks[1].setX(player2.x)
        playerMasks[1].setY(player2.y)
        pmask.draw(win)
        livesNumberLabel.draw(win, lives)
        livesLabel.draw(win)
        itLabel.draw(win)
        timeLabel.draw(win)
        pygame.display.update()

    def checkCollisions(
        player, player2, platform_main, platform_high_1, platform_high_2, platform_high_3, platform_high_4, pmask, lives
    ):
        """Function that controls collision detection and scoring based on collisions"""
        # Defining collision variables for each platform
        groundcollision_main = False
        groundcollision_high_1 = False
        groundcollision_high_2 = False
        groundcollision_high_3 = False
        groundcollision_high_4 = False

        # Collision logic for main platform
        if player.rect.colliderect(platform_main.rect):
            groundcollision_main = True
        if groundcollision_main:
            player.y_vel = 0
            player.gravity = 0
            player.rect.y = platform_main.rect.y - player.height
            pmask.setY(platform_main.rect.y - 50)

        # Collision logic for left high platform
        if player.rect.colliderect(platform_high_1.rect):
            groundcollision_high_1 = True
        if groundcollision_high_1:
            player.y_vel = 0
            player.gravity = 0
            player.rect.y = platform_high_1.rect.y - player.height
            pmask.setY(platform_high_1.rect.y - 50)

        # Collision logic for right high platform
        if player.rect.colliderect(platform_high_2.rect):
            groundcollision_high_2 = True
        if groundcollision_high_2:
            player.y_vel = 0
            player.gravity = 0
            player.rect.y = platform_high_2.rect.y - player.height
            pmask.setY(platform_high_2.rect.y - 50)

        # Collision logic for left VERY high platform
        if player.rect.colliderect(platform_high_3.rect):
            groundcollision_high_3 = True
        if groundcollision_high_3:
            player.y_vel = 0
            player.gravity = 0
            player.rect.y = platform_high_3.rect.y - player.height
            pmask.setY(platform_high_3.rect.y - 50)

        # Collision logic for left high platform
        if player.rect.colliderect(platform_high_4.rect):
            groundcollision_high_4 = True
        if groundcollision_high_4:
            player.y_vel = 0
            player.gravity = 0
            player.rect.y = platform_high_4.rect.y - player.height
            pmask.setY(platform_high_4.rect.y - 50)



        # Allows gravity when player is not on any platform
        if (
            not groundcollision_main
            and not groundcollision_high_1
            and not groundcollision_high_2
        ):
            while player.gravity < 0.3:
                player.gravity += 0.05

        # Handles collision detection between players and deducts a life from the player if they aren't It and resets time back to 20 seconds
        if player2.rect.colliderect(player.rect) or player.rect.colliderect(player2.rect):
            if player.getIt() == False:
                # If player isnt it, then deduct life, reset time and reset position
                timeLabel.seconds = 20
                player.x = 1640
                player.y = 100
                lives -= 1
                livesNumberLabel.setLives(lives)
                player.setLives(lives)
            elif player.getIt():
                # If player IS it then reset time and position
                timeLabel.seconds = 20
                player.x = 120
                player.y = 100

    def gameController():
        """Handles events that happen during gameplay"""
        # Globalizes lives
        global lives
        # Sets run to true to start the mainloop
        run = True
        # Defines the Network class as n
        n = network.Network()
        # Defines initial player position
        p = n.getP()
        # Defines the clock and timer variables
        clock = pygame.time.Clock()
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, 1000)
        # Sets players_landed to false to ensure no players get a head start and the timer is synced
        players_landed = False
        # Defining initial player lives
        p.setLives(lives)
        while run:
            clock.tick(60)
            # Sends position of player, and value returned by n.send is defined as p2 (the player 2 position)
            p2 = n.send(p)
            playerMasks[0].setX(p.getX())
            playerMasks[0].setY(p.getY())
            pygame.display.flip()
            # Updates the livesNumberLabel object
            livesNumberLabel.update()
            # Allows movement and starts the clock if players have both landed
            if p.y >= 589 and p2.y >= 589:
                players_landed = True
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                elif event.type == timer_event:
                    # Starts clock
                    if players_landed:
                        timeLabel.seconds -= 1
                        timeLabel.update()
            # Resets time to 20 when it reaches 0
            if timeLabel.seconds == 20 and not p.y == 100 and not p2.y == 100:
                goSound.play()
            if timeLabel.seconds == 0:
                if p.getIt():    
                    lives -= 1
                    livesNumberLabel.setLives(lives)
                    p.setLives(lives)
                    p.x = 1640
                    p.y = 100
                else:
                    p.x = 180
                    p.y = 100
                timeLabel.seconds = 20
            if p.y > width:
                timeLabel.seconds = 20
                lives -= 1
                livesNumberLabel.setLives(lives)
                p.setLives(lives)
                p.y = 100
            # If player lives equal zero, end game (lose)
            if p.getLives() == 0:
                youLose()
                run = False
                p.setLives(0)
                pygame.quit()
            # If player lives equal zero, end game (win)
            if p2.getLives() == 0:
                youWin()
                run = False
                pygame.quit()
            # Locks player position of 1 of the players is still hovering
            if p.y == 100 or p2.y == 100:
                if p.getIt():
                    p.x = 1640
                else:
                    p.x = 180
            # Sets label text to It or Not It
            if p.getIt():
                itLabel.text = "You are IT!"
            else:
                itLabel.text = "You are NOT IT!"
            # Calls the move() function in the player class
            p.move()
            # Calls the redrawWindow function which refreshes the screeen
            redrawWindow(
                win,
                background,
                p,
                p2,
                platform_main,
                platform_high_1,
                platform_high_2,
                platform_high_3,
                platform_high_4,
                playerMasks[0],
                lives,
            )
        if run == False:
            win.blit(background, (0, 0))
            gameOverLabel.draw(win)

    # Calls the gameController on run of the playingScreen function
    gameController()


def triggerGameStart():
    """Function that controls the start of the playingScreen()"""
    try:
        playingScreen()
    # Debugger function and exception handler to prevent the network from binding to nothing
    except Exception as e:
        print(e)

def youLose():
    """Function that controls losing the game"""
    # Tkinter losing screen
    window = tkinter.Tk()
    window.title("You lose!")
    label = tkinter.Button(
    text="You lose:(",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    )   
    label.pack()
    tkinter.mainloop()

def youWin():
    """Function that controls losing the game"""
    # Tkinter winning screen
    window = tkinter.Tk()
    window.title("You win!")
    label = tkinter.Button(
    text="You win!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    )   
    label.pack()
    tkinter.mainloop()


def main():
    """Mainline logic"""
    # MainMenu() runs while the play button is not pressed
    mainMenu()

# Call main
main()

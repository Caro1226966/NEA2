import pygame
import random
import math
import time
import tkinter as tk

# Screen Parameters (DON'T CHANGE)
root = tk.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
root.destroy()
BG_IMAGE_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Top Down Shooter Game')

# Fonts
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', int(round(SCREEN_WIDTH/38.5, 0)))
print(int(round(SCREEN_WIDTH/38.5, 0))) # Try to get it as close to 50 as possible on my monitor
score_font = pygame.font.SysFont('Comic Sans MS', int(round(SCREEN_WIDTH/9.6, 0)), bold=True)
print(int(round(SCREEN_WIDTH/9.6, 0))) # Try to get it as close to 200 as possible on my monitor

# initialisations
pygame.joystick.init()

# Constants (can be changed)------------------------------------------------
# Grid
GRID_SIZE = SCREEN_WIDTH/30

# Bullet Parameters
BULLET_LIFESPAN = 5
BULLET_VELOCITY = 30
BULLET_WIDTH = SCREEN_WIDTH/100
BULLET_HEIGHT = SCREEN_HEIGHT/100
BULLET_COOLDOWN = 15
BULLET_DAMAGE = 50

# player parameters
PLAYER_SPEED = SCREEN_WIDTH / 300
PLAYER_WIDTH = SCREEN_WIDTH / 30
PLAYER_HEIGHT = SCREEN_HEIGHT / 20

# Menu card parameters
CARD_WIDTH = SCREEN_WIDTH / 4
CARD_HEIGHT = SCREEN_HEIGHT / 1.5
print('Card Height: ', CARD_HEIGHT)
print('Card Width:', CARD_WIDTH)

# Monolith Parameters
MONOLITH_WIDTH = SCREEN_WIDTH / 15
MONOLITH_HEIGHT = SCREEN_HEIGHT / 10

# Zombie parameters
ZOMBIE_WIDTH = SCREEN_WIDTH/50
ZOMBIE_HEIGHT = SCREEN_HEIGHT / 30
ZOMBIE_SPAWN_PROBABILITY = 0.003
BASE_MOVEMENT_SPEED = SCREEN_WIDTH / 300
DEFAULT_ZOMBIE_COOLDOWN = 30

# Pointer Parameters
POINTER_SENSITIVITY = SCREEN_WIDTH / 200
POINTER_WIDTH = SCREEN_WIDTH / 60
POINTER_HEIGHT = SCREEN_HEIGHT / 40

# Wall Parameters
WALL_WIDTH = SCREEN_WIDTH/30
WALL_HEIGHT = SCREEN_HEIGHT/16.8

# Wall Item Parameters
WALL_ITEM_WIDTH = SCREEN_WIDTH/60
WALL_ITEM_HEIGHT = SCREEN_HEIGHT/32
WALL_MATERIAL_SPAWN_PROB = 700

# A constant to let the program know that the images have failed to load
IMAGE_LOADING_FAILED = False

# All Sprite Images (loaded here to prevent having to constantly load at runtime)
try:
    WALL_IMAGE = pygame.image.load('wall.png')
    MONOLITH_IMAGE = pygame.image.load('monolith.png')

    PLAYER_1_POINTER_IMAGE = pygame.image.load('player1_selector.png')
    PLAYER_2_POINTER_IMAGE = pygame.image.load('player2_selector.png')

    GRASSY_BACKGROUND = pygame.image.load('background.png')
    ZOMBIE_SHOOTER_BACKGROUND = pygame.image.load('zombie_menu_background.png')
    ZOMBIE_SHOOTER_MENU_CARD = pygame.image.load('zombie_shooter_menu_card.png')
except FileNotFoundError:
    print('One or more of the image files are missing or in the wrong location. Placeholders have been loaded ')
    IMAGE_LOADING_FAILED = True

    WALL_IMAGE = pygame.surface.Surface((WALL_WIDTH, WALL_HEIGHT))
    MONOLITH_IMAGE = pygame.surface.Surface((MONOLITH_WIDTH, MONOLITH_HEIGHT))
    PLAYER_1_POINTER_IMAGE =pygame.surface.Surface((POINTER_WIDTH, POINTER_HEIGHT))
    PLAYER_2_POINTER_IMAGE =pygame.surface.Surface((POINTER_WIDTH, POINTER_HEIGHT))
    GRASSY_BACKGROUND = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    ZOMBIE_SHOOTER_BACKGROUND =pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    ZOMBIE_SHOOTER_MENU_CARD =pygame.surface.Surface((CARD_WIDTH, CARD_HEIGHT))


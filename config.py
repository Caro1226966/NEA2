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

# Constants (can be changed)------------------------------------------------
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

# Monolith Parameters
MONOLITH_WIDTH = SCREEN_WIDTH / 15
MONOLITH_HEIGHT = SCREEN_HEIGHT / 10

# Zombie parameters
ZOMBIE_WIDTH = SCREEN_WIDTH/50
ZOMBIE_HEIGHT = SCREEN_HEIGHT / 30
REINFORCEMENT_PROBABILITY = 0.006
ZOMBIE_SPAWN_PROBABILITY = 0.003
BASE_MOVEMENT_SPEED = SCREEN_WIDTH / 300
DEFAULT_ZOMBIE_COOLDOWN = 30

# Pointer Parameters
POINTER_SENSITIVITY = SCREEN_WIDTH / 200
POINTER_WIDTH = SCREEN_WIDTH / 30
POINTER_HEIGHT = SCREEN_HEIGHT / 20


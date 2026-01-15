import pygame
import random
import math
import time
import tkinter as tk

# Screen Parameters (DON'T CHANGE)
root = tk.Tk()
root.winfo_screenwidth()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
root.destroy()
BG_IMAGE_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Top Down Shooter Game')

# Fonts
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 50)

# Constants (can be changed)
BULLET_LIFESPAN = 5

# player parameters
PLAYER_SPEED = SCREEN_WIDTH / 300
PLAYER_WIDTH = SCREEN_WIDTH / 30
PLAYER_HEIGHT = SCREEN_HEIGHT / 20

# Menu card parameters
CARD_WIDTH = SCREEN_WIDTH / 4
CARD_HEIGHT = SCREEN_HEIGHT / 1.5

# Monolith Parameters
MONOLITH_WIDTH = SCREEN_WIDTH / 8
MONOLITH_HEIGHT = SCREEN_HEIGHT / 3


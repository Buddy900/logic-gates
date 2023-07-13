import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.font.init()


WIDTH, HEIGHT = 1200, 800

FPS = 60

COLOURS = pygame.color.THECOLORS

NODE_FONT = pygame.font.SysFont("arial", 20)

MAX_RECURSION_DEPTH = 15

"""A module with helpful functions for creating game."""


import pygame as pg
from pygame.locals import *

screen_width = 750
screen_height = 750
screen = pg.display.set_mode((screen_width, screen_height))


def load_image(filename:str, erase_bg=True):
    image = pg.image.load('files\\' + filename).convert()

    if erase_bg is True:   # Make the background of the image transparrent
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(filename:str):
    return pg.mixer.Sound('files\\' + filename)


def draw_text(text:str, position:tuple, font:object, rgb_color:tuple):
    """Draw the text on the screen and return the rectangle in the position of the text."""
    text_obj = font.render(text, 1, rgb_color)
    text_rect = text_obj.get_rect()
    text_rect.center = position
    screen.blit(text_obj, text_rect)
    return text_rect

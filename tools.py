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


def draw_lifes(lifes):
    """Draw lifes of the player on the screen."""
    full_heart = pg.transform.scale(load_image('heart.png'), (80, 80))
    empty_heart = pg.transform.scale(load_image('heart.png'), (80, 80))
    empty_heart.set_alpha(90)
    heart_rect1 = full_heart.get_rect()
    heart_rect2 = full_heart.get_rect()
    heart_rect3 = full_heart.get_rect()
    heart_rect1.topleft = (510, 0)
    heart_rect2.topleft = (590, 0)
    heart_rect3.topleft = (670, 0)

    if lifes == 0:
        screen.blit(empty_heart, heart_rect1)
        screen.blit(empty_heart, heart_rect2)
        screen.blit(empty_heart, heart_rect3)
    if lifes == 1:
        screen.blit(full_heart, heart_rect1)
        screen.blit(empty_heart, heart_rect2)
        screen.blit(empty_heart, heart_rect3)
    if lifes == 2:
        screen.blit(full_heart, heart_rect1)
        screen.blit(full_heart, heart_rect2)
        screen.blit(empty_heart, heart_rect3)
    if lifes == 3:
        screen.blit(full_heart, heart_rect1)
        screen.blit(full_heart, heart_rect2)
        screen.blit(full_heart, heart_rect3)

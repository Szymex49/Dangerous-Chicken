"""A module with helpful functions for creating game."""


import pygame as pg
from pygame.locals import *
import os
import sys
import pickle
import math
import random
import datetime

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

MUSIC_VOLUME = 0.2
SOUNDS_VOLUME = 0.3

ranking_file = open('files\\ranking', 'rb')
RANKING = pickle.load(ranking_file)
ranking_file.close()


def load_image(filename:str, erase_bg=True):
    image = pg.image.load('files\\' + filename).convert()

    if erase_bg is True:   # Make the background of the image transparrent
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(filename:str, volume=0.5):
    sound = pg.mixer.Sound('files\\' + filename)
    sound.set_volume(volume)
    return sound


def play_music(filename:str, volume=0.5):
    """Play looped music from a file."""
    pg.mixer.music.load('files\\' + filename)
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(-1)


def draw_text(text:str, position:tuple, font:object, rgb_color:tuple):
    """Draw the text on the screen and return the rectangle in the position of the text."""
    text_obj = font.render(text, 1, rgb_color)
    text_rect = text_obj.get_rect()
    text_rect.center = position
    SCREEN.blit(text_obj, text_rect)
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
        SCREEN.blit(empty_heart, heart_rect1)
        SCREEN.blit(empty_heart, heart_rect2)
        SCREEN.blit(empty_heart, heart_rect3)
    if lifes == 1:
        SCREEN.blit(full_heart, heart_rect1)
        SCREEN.blit(empty_heart, heart_rect2)
        SCREEN.blit(empty_heart, heart_rect3)
    if lifes == 2:
        SCREEN.blit(full_heart, heart_rect1)
        SCREEN.blit(full_heart, heart_rect2)
        SCREEN.blit(empty_heart, heart_rect3)
    if lifes == 3:
        SCREEN.blit(full_heart, heart_rect1)
        SCREEN.blit(full_heart, heart_rect2)
        SCREEN.blit(full_heart, heart_rect3)
    

def update_ranking(score):
    """Add new score to the ranking and remove the the score on the last position."""
    global RANKING
    date = str(datetime.date.today())
    date = date.replace('-', '.')
    RANKING[score] = date   # New score
    RANKING = {key:RANKING[key] for key in sorted(RANKING.keys())[-5:]}  # Add new score and sort

    os.remove('files\\ranking')
    ranking_file = open('files\\ranking', 'wb')
    pickle.dump(RANKING, ranking_file)
    ranking_file.close()

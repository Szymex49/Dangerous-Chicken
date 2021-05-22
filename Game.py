import pygame as pg

pg.init()
screen = pg.display.set_mode((600, 600))
pg.display.set_caption("fajna gra")
pg.display.flip()

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

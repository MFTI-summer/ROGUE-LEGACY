import pygame as pg
pg.init()

walk = pg.mixer.Sound('Sounds/Sound_Walk_Castle_short.ogg')

while 1:
    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_a or e.key == pg.K_d:
                walk.play()
            

import pygame as pg
import Tiles
import Hero

if __name__ == '__main__':

    WIN_width = 750
    WIN_height = 500

    run = True
    fps: int = 60

    display = pg.display.set_mode((WIN_width, WIN_height))
    clock = pg.time.Clock()

    hero = Hero.Hero()

    hero.rect.x = 300
    hero.rect.y = 300

    level = Tiles.Level(Tiles.level_10_map)
    hero.set_level(level)

    while run:

        display.fill([0] * 3)

        hero.update(display)
        level.update(display)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        pg.display.update()
        clock.tick(fps)

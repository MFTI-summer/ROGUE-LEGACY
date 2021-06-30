import pygame as pg
import Tiles
import Hero
import UI

if __name__ == '__main__':

    WIN_width = 750
    WIN_height = 500

    run = True
    fps: int = 60

    display = pg.display.set_mode((WIN_width, WIN_height))
    clock = pg.time.Clock()

    hero = Hero.Hero(x=300, y=300)

    # hero.rect.x = 300
    # hero.rect.y = 300
    ui = UI.UI(hero, 5, WIN_height-5)
    level = Tiles.Level(Tiles.level_10_map)
    hero.set_level(level)

    while run:
        events = pg.event.get()
        display.fill([0] * 3)
        ui.update()
        hero.update(display, events=events)
        level.update(display)
        ui.display(display)
        for event in events:
            if event.type == pg.QUIT:
                run = False
        pg.display.update()
        clock.tick(fps)

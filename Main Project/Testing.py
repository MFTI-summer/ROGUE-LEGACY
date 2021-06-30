import pygame as pg
import pygame.event
import Item
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
    heal_potion = Item.HealItem(30, 100, 100)
    hero = Hero.Hero(x=300, y=300)
    ui = UI.UI(hero, 5, WIN_height-5)
    ui.heal_slot.store_item(heal_potion)
    # hero.rect.x = 300
    # hero.rect.y = 300
    level = Tiles.Level(Tiles.level_12_map)
    hero.set_level(level)
    hero.damage(30)
    while run:
        events = pg.event.get()
        display.fill([0] * 3)
        hero.update(display, events=events)
        level.update(display)
        for event in events:
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pygame.K_e:
                    ui.mana_slot.use_item()
                if event.key == pygame.K_q:
                    ui.heal_slot.use_item()
        ui.update()
        ui.display(display)
        pg.display.update()
        clock.tick(fps)

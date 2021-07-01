import pygame as pg
import pygame.event
import Item
import Tiles
import Hero
import UI

pg.mixer.init()

if __name__ == '__main__':

    MANA_RESTORED_FOR_TICK = 5

    WIN_width = 750
    WIN_height = 500

    run = True
    fps: int = 60

    walk = pg.mixer.Sound('Sounds/Sound_collide_and_walk.wav')
    collide = pg.mixer.Sound('Sounds/Sound_collide_and_walk.wav')
    shut = pg.mixer.Sound('Sounds/Sound_Hit_Enemy.ogg')
    damage = pg.mixer.Sound('Sounds/Sound_Hit_hero.ogg')
    can_play = True
    
    display = pg.display.set_mode((WIN_width, WIN_height))
    clock = pg.time.Clock()
    heal_potion = Item.HealItem(30)
    mana_potion = Item.RestoreManaItem(50)
    hero = Hero.Hero(x=300, y=300)
    ui = UI.UI(hero, 5, WIN_height-5)
    for _ in range(10):
        ui.heal_slot.store_item(heal_potion)
        ui.mana_slot.store_item(mana_potion)
    # hero.rect.x = 300
    # hero.rect.y = 300
    level = Tiles.Level(Tiles.level_12_map)
    hero.set_level(level)
    hero.damage(30)
    while run:
        hero.restore_mana(MANA_RESTORED_FOR_TICK/fps)
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
                if event.key == pg.K_a or event.key == pg.K_d:
                    walk.play()
                if event.key == pg.K_SPACE:
                    can_play = True
        for tile in hero.level.level:
            if hero.rect.bottom < tile.rect.top + 10 and can_play == True:
                collide.play()
                if hero.current_speed['y'] == 0:
                    can_play = False
                    break
        ui.update()
        ui.display(display)
        pg.display.update()
        clock.tick(fps)

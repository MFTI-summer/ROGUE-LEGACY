import pygame





bg = pygame.image.load("Tiles/bg/bg.png")
bg = pygame.transform.scale(bg, (bg.get_width()//2, bg.get_height()//2))

display = pygame.display.set_mode((bg.get_width(), bg.get_height()))


hero = pygame.image.load("Tiles/Character/Animations/Attack/Armature_Attack_00.png")
hero = pygame.transform.scale(hero, (hero.get_width()//3, hero.get_height()//3))

hero_rect = hero.get_rect(x = 300, bottom=bg.get_height())


game = True
while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                hero_rect.x += 5
            if event.key == pygame.K_LEFT:
                hero_rect.x -= 5

            if event.key == pygame.K_UP:
                hero_rect.top = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            hero_rect.y += 20


    display.blit(bg, (0,0))
    display.blit(hero, hero_rect)
    pygame.display.update()
pygame.quit()

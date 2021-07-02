import pygame
from random import randint as ri

window_widht = 1000
window_height = 500


class Enemy(pygame.sprite.Sprite):
    walkRight = [pygame.image.load(f'Animations/Enemy/R{i}E.png') for i in range(1, 11 + 1)]
    walkLeft = [pygame.image.load(f'Animations/Enemy/L{i}E.png') for i in range(1, 11 + 1)]

    def __init__(self, x, bottom, groups, end=400):
        super().__init__(groups)

        # координаты, на которых появляется моб
        self.end = end
        self.borders: pygame.sprite.Group() = None
        self.direction = 1  # влево или вправо
        self.walkCount = 0  # нужно для корректной отрисовки анимации
        self.image = self.walkRight[self.walkCount // 3]
        self.rect = self.image.get_rect(x=x, y=bottom - 64)
        self.path = [self.rect.x, self.end]  # та траектория, по которой он гуляет
        self.vel = 3  # скорость
        # self.hitbox = (self.x + 17, self.y + 2, 31, 57) #размеры его хитбокса(я пытался их максимально подогнать к рамерам текстуры)
        self.health = 100
        self.isAlive = True

    def update(self):
        # if not self.isAlive:
        #     self.kill()
        self.move()
        self.animation()

    def move(self):
        if self.collide_x():
            self.vel *= -1
        self.rect.x += self.vel

    def animation(self):
        self.walkCount += 1
        idx = (self.walkCount % (len(self.walkRight) * 3)) // 3
        if self.vel < 0:  # Влево
            self.image = self.walkLeft[idx]
        elif self.vel > 0: # вправо
            self.image = self.walkRight[idx]
    # def animation(self):
    #     self.move()
    #     if self.isAlive:  # отрисовка персонажа, при условии, что тот жив
    #         if self.walkCount + 1 >= 33:
    #             self.walkCount = 0
    #
    #         if self.vel > 0:
    #             self.image = self.walkRight[self.walkCount // 3]
    #             # win.blit(, (self.x, self.y))
    #             self.walkCount += 1
    #         else:
    #             self.image = self.walkLeft[self.walkCount // 3]
    #             # win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
    #             self.walkCount += 1
    #
    # def move(self):  # движение персонажа по заданной траектории
    #     if self.vel > 0:
    #         if self.rect.x + self.vel < self.path[1]:
    #             self.rect.x += self.vel
    #         else:
    #             self.vel = self.vel * -1
    #             self.walkCount = 0
    #     else:
    #         if self.rect.x - self.vel > self.path[0]:
    #             self.rect.x += self.vel
    #         else:
    #             self.vel = self.vel * -1
    #             self.walkCount = 0

    def collide_x(self):
        if pygame.sprite.spritecollideany(self, self.borders) is not None:
            return True


    def set_borders(self, borders):
        self.borders = borders

    def get_damage(self, gotten_damage):
        if self.health - gotten_damage <= 0:
            self.isAlive = False
        else:
            self.health -= gotten_damage

    def attack(self):
        pass


class Ghost(Enemy):
    def __init__(self, x, bottom, end=400):
        super(Ghost, self).__init__(x, bottom, end=end)


enemys = pygame.sprite.Group()


def main():
    display = pygame.display.set_mode((window_widht, window_height))
    clock = pygame.time.Clock()
    run = True
    for _ in range(5):
        Enemy(groups=enemys, x=20, bottom=ri(0, 450), end=400)

    while run:
        display.fill([255] * 3)
        enemys.draw(display)
        enemys.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()

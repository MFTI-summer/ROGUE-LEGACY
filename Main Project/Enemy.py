import pygame
from random import randint as ri

window_widht=1000
window_height=500


class Enemy(pygame.sprite.Sprite):
    walkRight = [pygame.image.load('Animations/Enemy/R1E.png'), pygame.image.load('Animations/Enemy/R2E.png'), pygame.image.load('Animations/Enemy/R3E.png'), pygame.image.load('Animations/Enemy/R4E.png'), pygame.image.load('Animations/Enemy/R5E.png'), pygame.image.load('Animations/Enemy/R6E.png'), pygame.image.load('Animations/Enemy/R7E.png'), pygame.image.load('Animations/Enemy/R8E.png'), pygame.image.load('Animations/Enemy/R9E.png'), pygame.image.load('Animations/Enemy/R10E.png'), pygame.image.load('Animations/Enemy/R11E.png')]
    walkLeft = [pygame.image.load('Animations/Enemy/L1E.png'), pygame.image.load('Animations/Enemy/L2E.png'), pygame.image.load('Animations/Enemy/L3E.png'), pygame.image.load('Animations/Enemy/L4E.png'), pygame.image.load('Animations/Enemy/L5E.png'), pygame.image.load('Animations/Enemy/L6E.png'), pygame.image.load('Animations/Enemy/L7E.png'), pygame.image.load('Animations/Enemy/L8E.png'), pygame.image.load('Animations/Enemy/L9E.png'), pygame.image.load('Animations/Enemy/L10E.png'), pygame.image.load('Animations/Enemy/L11E.png')]

    def __init__(self, groups, x, y, end):
        super().__init__(groups)


        #координаты, на которых появляется моб
        self.end = end
        self.walkCount = 0   #нужно для корректной отрисовки анимации
        self.image = self.walkRight[self.walkCount //3]
        self.rect = self.image.get_rect(x=x, y=y)
        self.path = [self.rect.x, self.end]#та траектория, по которой он гуляет
        self.vel = 3    #скорость
        #self.hitbox = (self.x + 17, self.y + 2, 31, 57) #размеры его хитбокса(я пытался их максимально подогнать к рамерам текстуры)
        self.health=100
        self.isAlive=True

    def update(self):
        # if not self.isAlive:
        #     self.kill()
        self.animation()


    def animation(self):
        self.move()
        if self.isAlive:#отрисовка персонажа, при условии, что тот жив
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                self.image = self.walkRight[self.walkCount //3]
                #win.blit(, (self.x, self.y))
                self.walkCount += 1
            else:
                self.image = self.walkLeft[self.walkCount //3]
                #win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1


    def move(self):#движение персонажа по заданной траектории
        if self.vel > 0:
            if self.rect.x + self.vel < self.path[1]:
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.rect.x - self.vel > self.path[0]:
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def get_damage(self, gotten_damage):
        if self.health-gotten_damage<=0:
            self.isAlive=False
        else:
            self.health-=gotten_damage
    def attack(self):
        pass

enemys = pygame.sprite.Group()

def main():
    display = pygame.display.set_mode((window_widht, window_height))
    clock = pygame.time.Clock()
    run = True
    for _ in range(5):
        Enemy(groups = enemys, x=20,y=ri(0, 450), end=400)


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



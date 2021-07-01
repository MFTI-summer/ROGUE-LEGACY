import pygame
class Enemy():
    walkRight = [pygame.image.load('Animations/Enemy/R1E.png'), pygame.image.load('Animations/Enemy/R2E.png'), pygame.image.load('Animations/Enemy/R3E.png'), pygame.image.load('Animations/Enemy/R4E.png'), pygame.image.load('Animations/Enemy/R5E.png'), pygame.image.load('Animations/Enemy/R6E.png'), pygame.image.load('Animations/Enemy/R7E.png'), pygame.image.load('Animations/Enemy/R8E.png'), pygame.image.load('Animations/Enemy/R9E.png'), pygame.image.load('Animations/Enemy/R10E.png'), pygame.image.load('Animations/Enemy/R11E.png')]
    walkLeft = [pygame.image.load('Animations/Enemy/L1E.png'), pygame.image.load('Animations/Enemy/L2E.png'), pygame.image.load('Animations/Enemy/L3E.png'), pygame.image.load('Animations/Enemy/L4E.png'), pygame.image.load('Animations/Enemy/L5E.png'), pygame.image.load('Animations/Enemy/L6E.png'), pygame.image.load('Animations/Enemy/L7E.png'), pygame.image.load('Animations/Enemy/L8E.png'), pygame.image.load('Animations/Enemy/L9E.png'), pygame.image.load('Animations/Enemy/L10E.png'), pygame.image.load('Animations/Enemy/L11E.png')]

    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        #координаты, на которых появляется моб
        self.end = end
        self.path = [self.x, self.end]#та траектория, по которой он гуляет
        self.walkCount = 0   #нужно для корректной отрисовки анимации
        self.vel = 3    #скорость
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) #размеры его хитбокса(я пытался их максимально подогнать к рамерам текстуры)
        self.health=100
        self.isAlive=True

    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def get_damage(self, gotten_damage):
        if self.health-gotten_damage<=0:
            self.isAlive=False
        else:
            self.health-=gotten_damage



import pygame
import sys
import random

WIN_WIDTH = 400
WIN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)


x = 160
y = 680

FPS = 60

STOP = "stop"

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 0))


surf1 = pygame.image.load('D:/Изучение языков программирования и разметки/Python/Фон.png')
surf1_rect = surf1.get_rect(center=(0, 0))
ball1 = Ball(random.randint(1, WIN_WIDTH), 'D:/!!!ЗАГРУЗКИ/Шар.png')

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                x -= 20
            elif i.key == pygame.K_RIGHT:
                x += 20
    if ball1.rect.y < WIN_HEIGHT:
        ball1.rect.y += 3
    if surf1_rect.colliderect(ball1.rect):
        ball1.rect.y = random.randint(30, 370)
        ball1.rect.x = random.randint(50, 650)
    screen.fill(LIGHT_BLUE)
    screen.blit(surf1, (x, y))
    screen.blit(ball1.image, ball1.rect)
    pygame.display.update()
    clock.tick(FPS)

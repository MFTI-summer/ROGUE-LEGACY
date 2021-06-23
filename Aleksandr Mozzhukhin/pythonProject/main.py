import pygame
import random
pygame.init()

win=pygame.display.set_mode((500, 480))

pygame.display.set_caption("Test Game")

texture_background=pygame.image.load("stars-texture-background.jpg")
char1=pygame.image.load("character.png")
char2=pygame.image.load("character2.png")
danger=pygame.image.load("asteroid.png")

class player1(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel=15
        self.hitbox=(self.x+10, self.y, 28, 50 )
    def draw(self, win):
        win.blit(char1, (self.x, self.y))
        self.hitbox = (self.x+10, self.y, 30, 50)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)



class player2(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel=15
        self.hitbox=(self.x+10, self.y, 28, 50)
    def draw(self, win):
        win.blit(char2, (self.x, self.y))
        self.hitbox = (self.x + 20, self.y-7, 25, 40)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


class asteroid(object):
    def __init__(self, x, y, width, height, end):
        self.x=x
        self.y=y
        self.widht=width
        self.height=height
        self.end=end
        self.path=[self.y, self.end]
        self.vel=10
        self.hitbox = (self.x + 7, self.y, 25, 50)
    def draw(self, win):
        self.move()
        win.blit(danger, (self.x, self.y))
        self.hitbox = (self.x + 10, self.y, 25, 50)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel>0:
            if self.y+self.vel<self.path[1]:
                self.y+=self.vel
            else:
                self.vel=self.vel*-1
        else:
            if self.y-self.vel>self.path[0]:
                self.y+=self.vel
            else:
                self.vel=self.vel*-1
    def hit(self):
        print("+1")

def redrewGameWindow():
    win.blit(texture_background, (0, 0))
    man1.draw(win)
    man2.draw(win)
    asteroid.draw(win)
    pygame.display.update()

#main part
man1=player1(0, 0, 50, 45)
man2=player2(0,450, 69,43)
asteroid=asteroid(random.randint(0,450), 0, 50, 50, 450)
run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    if asteroid.y+asteroid.height<man1.hitbox[1]+man1.hitbox[3]:
        if asteroid.x +asteroid.widht>man1.hitbox[0]:
            asteroid.hit()
    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man1.x>man1.vel:
        man1.x-=man1.vel
    if keys[pygame.K_RIGHT] and man1.x< 510-man1.width-man1.vel:
        man1.x+=man1.vel
    if keys[pygame.K_a] and man2.x>0:
        man2.x-=man2.vel
    if keys[pygame.K_d]  and man2.x< 500-man2.width-man2.vel:
        man2.x+=man2.vel

    redrewGameWindow()
pygame.quit()
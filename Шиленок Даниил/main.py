import pygame
import sys
import random
import time

# ----COLORS------
WHITE = (255, 255, 255)
BLUE = (0, 0, 225)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 85, 15)
LIGHT_BLUE = (98, 91, 255)

# ----DISPLAY-----
FPS = 60
W = 500  # ширина экрана
H = 700  # высота экрана
BG_COLOR = LIGHT_BLUE

# ----PLATFORM----
W_OF_PLATFORM = 100
H_OF_PLATFORM = 20
Y_OF_PLATFORM = H - 80
COLOR_OF_PLATFORM = BLUE
SPEED_OF_PLATFORM = 5

# ----BLOCK-------
W_OF_BLOCK = 70
H_OF_BLOCK = 25
X_COUNT = 5
Y_COUNT = 4
X_DISTANCE_BTW_BLOCKS = 20
Y_DISTANCE_BTW_BLOCKS = 30
BLOCK_X_FROM_START = 40
BLOCK_Y_FROM_START = 30

# ----BALL--------
COLOR_OF_BALL = WHITE
RADIUS = 5
SPEED_OF_BALL = 5


class Ball():
    surf = pygame.Surface((5, 5))

    def __init__(self, startpos, velocity, startdir):
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        self.rect = self.surf.get_rect(center=(round(self.pos.x), round(self.pos.y)))

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)


class Block():
    color = RED
    _durability = 3
    _lastCollisionTime = -1

    def __init__(self, startpos):
        self.pos = pygame.math.Vector2(startpos)

    def damage(self):
        if self._lastCollisionTime == -1:
            _lastCollisionTime = time.time()
        if time.time()-self._lastCollisionTime > 0.1:
            self._durability -= 1
            self.update()
            self._lastCollisionTime = time.time()
        return self._durability

    def update(self):
        if self._durability == 2:
            self.color = BLUE
        elif self._durability == 1:
            self.color = GREEN


# -----INIT------
pygame.init()
pygame.display.set_caption('Арканоид')
font = pygame.font.Font(None, 72)
gameOver = font.render("GAME OVER", True, (255, 0, 0))
gameWin = font.render("YOU WIN", True, (255, 255, 255))
ball = Ball((250, 250), SPEED_OF_BALL, (random.random(), random.random()))
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
blocks = []
for a in range(Y_COUNT):
    for b in range(X_COUNT):
        blocks.append(Block((b * W_OF_BLOCK + b * X_DISTANCE_BTW_BLOCKS + BLOCK_X_FROM_START,
                             a * H_OF_BLOCK + a * Y_DISTANCE_BTW_BLOCKS + BLOCK_Y_FROM_START)))

x = W / 2  # start x of platform

# ----------START---------------
while True:
    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(BG_COLOR)

    # ---------BLOCKS\REFLECTIONS---------
    for block in blocks:
        if block.pos.x + W_OF_BLOCK-2 < ball.rect.left <= block.pos.x + W_OF_BLOCK+3 and block.pos.y - 1 <= ball.rect.top <= block.pos.y + H_OF_BLOCK + 1:
            ball.reflect((1, 0))
            if block.damage() == 0:
                blocks.remove(block)
        elif block.pos.x-3 <= ball.rect.right < block.pos.x + 2 and block.pos.y - 1 <= ball.rect.top <= block.pos.y + H_OF_BLOCK + 1:
            ball.reflect((-1, 0))
            if block.damage() == 0:
                blocks.remove(block)
        elif block.pos.y + H_OF_BLOCK - 5 <= ball.rect.top < block.pos.y + H_OF_BLOCK and block.pos.x - 1 <= ball.rect.left <= block.pos.x + W_OF_BLOCK + 1:
            ball.reflect((0, 1))
            if block.damage() == 0:
                blocks.remove(block)
        elif block.pos.y <= ball.rect.bottom < block.pos.y + 5 and block.pos.x - 1 <= ball.rect.left <= block.pos.x + W_OF_BLOCK + 1:
            ball.reflect((0, -1))
            if block.damage() == 0:
                blocks.remove(block)
        pygame.draw.rect(sc, block.color, (block.pos.x, block.pos.y, W_OF_BLOCK, H_OF_BLOCK))

    # -------------WIN-------------------
    if len(blocks) == 0:
        sc.fill(BG_COLOR)
        endTime = time.time()
        while time.time() - endTime < 5:
            sc.blit(gameWin, gameWin.get_rect(center=(W / 2, H / 2)))
            pygame.display.update()
        sys.exit()

    # -------WALL-REFLECTIONS------------
    if ball.rect.left <= 0:
        ball.reflect((1, 0))
    if ball.rect.right >= W:
        ball.reflect((-1, 0))
    if ball.rect.top <= 0:
        ball.reflect((0, 1))
    if Y_OF_PLATFORM <= ball.rect.bottom < Y_OF_PLATFORM + 5:
        if x - 2 < ball.rect.centerx < x + 2 + W_OF_PLATFORM:
            ball.reflect((0, -1))
    if ball.rect.bottom > Y_OF_PLATFORM + 5:
        sc.blit(gameOver, gameOver.get_rect(center=(W / 2, H / 2)))
    ball.update()
    pygame.draw.circle(sc, COLOR_OF_BALL, pygame.Vector2(ball.pos.x, ball.pos.y), RADIUS)
    pygame.draw.rect(sc, COLOR_OF_PLATFORM, (x, Y_OF_PLATFORM, W_OF_PLATFORM, H_OF_PLATFORM))

    # -------PLATFORM_MOVEMENT-----------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if x >= 0:
            x -= SPEED_OF_PLATFORM
    elif keys[pygame.K_RIGHT]:
        if x <= W - W_OF_PLATFORM:
            x += SPEED_OF_PLATFORM
    pygame.display.update()

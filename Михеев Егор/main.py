import math
import pygame as pg
import sys

BLACK = [0] * 3
WHITE = [255] * 3
GRAY =  [125] * 3

WIN_width = 650
WIN_height = 450

FONT_SIZE = 25

a = 0.2

class Player:
    padding = 10
    width = 15
    height = 62.83 * 1.5  # 20pi * 1.5 (for bigger rocket) = 30 pi
    score = 0

    def __init__(self, screen, x):
        self.screen = screen
        self.x = x
        self.y = 0

    def redraw(self, y):
        self.y = y
        pg.draw.rect(self.screen, WHITE, [self.x, y, self.width, self.height])


class Enemy(Player):
    def __init__(self, screen, x):
        Player.__init__(self, screen, x)

    def follow_ball(self, ball):
        # return's 1, -1, or 0
        self.dy = ball.y - self.y
        possible_redo = 1.5
        # if dy < 0 and dy < possible_redo * (-1):
        # return -1
        # elif possible_redo * (-1) < dy < possible_redo:
        # return int (0)
        # elif dy > 0 and dy > possible_redo:
        # return 1
        if ball.y > self.y and self.dy > possible_redo:
            return 1
        elif ball.y < self.y and self.dy < possible_redo * (-1):
            return -1
        else:
            return 0
        # elif ball.y == self.y:
        # return 0


class Ball:
    x = WIN_width // 2
    y = WIN_height // 2

    def __init__(self, screen, radius):
        self.r = radius
        self.screen = screen

    def redraw(self, x, y) -> object:
        """Просто рисует мячик с новыми координатами"""
        # Заодно обновим координаты, это будет нужно для коллизий
        self.x = x
        self.y = y
        # Собственно рисуем
        pg.draw.circle(self.screen, WHITE, [x, y], self.r)

    def check_collision_with_rocket(self, p1: Player, p2: Player):  # p1 - me, p2 - enemy
        """Проверяет столкновения с рокетками и возвращает правду или ложь"""

        if self.x - self.r <= Player.width and self.x + self.r > Player.padding:
            if p1.y - self.r < self.y < p1.y + Player.height + self.r:
                return True
        elif self.x + self.r >= WIN_width - Player.width and self.x - self.r < WIN_width - Player.padding:
            if p2.y - self.r <= self.y <= p2.y + p2.height + self.r:
                return True
        else:
            return False

        # return's True or False

    def check_collision_with_boarder(self):  # проверяем, столкнулся ли шарик с границами поля
        if self.y + self.r > WIN_height or self.y - self.r < 0:
            return True  # Если да, то, как будет видно из дельнейшего кода,
            # мы просто меняем вертикальное направление движения мачика

    def find_angle(self, p_y: float):
        # dy = (p_y + Player.height / 2) - self.y
        dy = (Player.height / 2 - (self.y - p_y))  # на каком расстоянии от середины ракетки коснулся шарик
        # Размер ракетки - 30 pi, а синусы работают только с долями pi
        # Значит нам нужно отклонение поделить на 30
        sin = math.sin(abs(dy) / 30)

        return [sin, 1] if dy < 0 else [sin, -1]  # Сохраняем знак отскока

    def win(self, left_player, right_player):
        if self.x <= 0:
            right_player.score += 1
            return True
        elif self.x >= WIN_width:
            left_player.score += 1
            return True
        else:
            return False


def sigmoid(x):
    return 1 / (1 + 2.701 ** (-1 * x))

def draw_pretty(screen,  n: int, color:tuple):

    lenght = WIN_height / n
    widht = 11
    x = (WIN_width - widht) / 2
    y = lenght / 2
    for i in range (n):
        pg.draw.rect(screen, color, [x, y, widht, lenght])
        y += 2 * lenght

def draw_score(screen, color, size, score_left, score_right, font=None):
    f = pg.font.SysFont('serif', 36)

def main():
    # Пишу комменты для себя, поэтому на русском
    # Определяем размеры переменные
    x_ball = WIN_width // 2
    y_ball = WIN_height // 2
    r = 12
    # Определяем переменные скорости мячика
    speed_x = -6
    speed_y = 0
    max_y = 7  # Максимальная скорость, с которой может летать шарик по вертикали
    # (нужно для корректной работы тригонометрических функций)

    # теперь определяемся с ракетками
    my_y = WIN_height // 2
    enemy_y = (WIN_height - 100)//2
    rocket_speed = 5

    fps = 60

    # А тут все системно важные переменные
    pg.font.init()
    screen = pg.display.set_mode((WIN_width, WIN_height))
    clock = pg.time.Clock()
    me = Player(screen, Player.padding)
    enemy = Enemy(screen, WIN_width - Player.width - Player.padding)
    ball = Ball(screen, r)

    while 1:
        # рисуем все на экране (по сути обновляем кадр)
        if ball.win(me, enemy):
            enemy_y = (WIN_width - Player.height) // 2
            my_y = WIN_height // 2 - Player.height // 2
            x_ball = WIN_width // 2
            y_ball = WIN_height // 2
            if speed_x < 0:
                speed_x = -6
            else:
                speed_x = 6

        screen.fill(BLACK)
        draw_pretty(screen, 12, GRAY)
        draw_score(screen, GRAY, 36, me.score, enemy.score)
        me.redraw(my_y)
        enemy.redraw(enemy_y)
        ball.redraw(x_ball, y_ball)

        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
        # Получаем зажатые клавиши
        pressed_keys = pg.key.get_pressed()
        # Тут я настраиваю управление игроком
        if pressed_keys[pg.K_UP] and my_y - rocket_speed >= 0:
            my_y -= rocket_speed
        if pressed_keys[pg.K_DOWN] and (my_y + Player.height) + rocket_speed <= WIN_height:
            my_y += rocket_speed
        # Знаю, что не очень красиво выглядит, но дело в том, что я не знаю как переименовать функцию
        # так, чтобы она подразумевала булевый ответ и при этом было понятно, что она делает
        if ball.check_collision_with_rocket(me, enemy):
            speed_x *= -1
            if speed_x > 0:
                angle = ball.find_angle(me.y)
                speed_y = (max_y * angle[0]) * angle[1]
            else:
                angle = ball.find_angle(enemy.y)
                speed_y = (max_y * angle[0]) * angle[1]

            if speed_x < 0:
                speed_x -= a
            else:
                speed_x += a
        else:
            pass

        if ball.check_collision_with_boarder():
            speed_y *= -1
        print(speed_x, speed_y)
        direction = enemy.follow_ball(ball)
        enemy_y += rocket_speed * direction * (1 - sigmoid(enemy.dy) / 3)
        if enemy_y + Player.height > WIN_height:
            enemy_y -= enemy_y + Player.height - WIN_height
        elif enemy_y < 0:
            enemy_y += 0 - enemy_y

        x_ball += speed_x
        y_ball += speed_y

        pg.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()

import pygame as pg

WIN_width = 1000
WIN_height = 500

fps = 60




class Hero(pg.sprite.Sprite):

    def __init__(self, x, y):
        # ща буит куча переменных, поэтому держись
        # Необходимые для анимации переменные
        self.facing = 0  # 0 - налево, 1 - направо
        self.animation = {  # Тут собраны все анимации, доступные герою
            'walk': [pg.image.load(f'Animations/Hero/Walk/L{frame}.png') for frame in range(1, 9)]  # ходьба
        }
        self.walk_state = 1  # то, в каком положении сейчас находится гг
        # Переменные для передвижения
        self.move_speed = {  # то, с какой скоростью герой может двигаться
            'x': 5,  # с какой скоростью герой бегает
            'y': 7  # с какой силой герой прыгает
        }
        self.current_speed = {
            'x': 0,
            'y': 0
        }

        self.is_jump = False  # Находится ли персонаж в прыжке
        # обязательные переменные
        pg.sprite.Sprite.__init__(self)  # Это необходимо для корректной работы класса
        self.image = self.animation['walk'][0]  # Пока поставим первое изображение ходьбы в качестве спокойствия
        #self.image = self.image.subsurface((20, 20, 50, 80)) #https://www.pygame.org/docs/ref/surface.html#pygame.Surface.subsurface
        self.rect = self.image.get_rect(x = x, y=y)
        self.level = None
        self.intersection = lambda y1, y2, l1, l2: (y1 - y2) + l2 >= 0 if (y1 - y2) > 0 else (y1 - y2) + l1 >= 0
        self.isCollided = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

    def update(self, surface: pg.surface.Surface, level=None):
        self.check_controls()
        self.image = self.get_frame()  # просчитываем кадр анимации
        self.draw(surface, self.image)

    def draw(self, surface: pg.surface.Surface, image):

        surface.blit(self.image, self.rect)

    def get_frame(self):  # Узнаем, на каком кадре находится анимация
        frame = int((self.walk_state // 3) % len(self.animation['walk']))
        return pg.transform.flip(self.animation['walk'][frame], self.facing, 0)

    def check_controls(self):
        """
        Изменяет координаты пероснажа, а также помогает с рассчетом анимации
        :return: Конкретное изображение из анимации героя
        """
        keys = pg.key.get_pressed()

        if keys[pg.K_d] and not self.isCollided['right']:  # вправо
            self.current_speed['x'] = self.move_speed['x']
            self.facing = 1
            self.walk_state += 1 / 3
            self.isCollided['left'] = False
            walls = pg.sprite.spritecollide(self, self.level.walls, dokill=False)
            for wall in walls:
                if self.intersection(self.rect.y, wall.rect.y, self.rect.h, wall.rect.h):
                    self.current_speed['x'] = wall.rect.left - self.rect.right
                    self.isCollided['right'] = True

        elif keys[pg.K_a] and not self.isCollided['left']:
            self.current_speed['x'] = self.move_speed['x'] * -1
            self.facing = 0
            self.walk_state += 1 / 3
            self.isCollided['right'] = False
            walls = pg.sprite.spritecollide(self, self.level.walls, dokill=False)
            for wall in walls:
                if self.intersection(self.rect.y, wall.rect.y, self.rect.h, wall.rect.h):
                    self.current_speed['x'] = 0
                    self.isCollided['left'] = True


        else:
            self.current_speed['x'] = 0
            self.walk_state = 1

        self.check_gravity(keys)  # Проверяем состояние прыжка

        self.rect.x += self.current_speed['x']

    def check_gravity(self, keys):
        """
        Вообще путь должен считать довольно простенько, принимая фиксированную скрость падения,
        чтобы всем было легко понять это движение, но я немного убитый, поэтому вот.
        Мы посчитаем его как интеграл скорости по времени(∫υ(Δt)Δt), где dt = 1/60 секунды
        (в принципе dt высчитывается как секунда, деленая на fps, просто у меня fps равен 60)
        Считаем интеграл мы только для большей реалистичности прыжка (а для меня это важно)
        :return:
        """
        # Вводим переменные для укорачивания записи
        g = 10  # сила гравитации, она же ускорение свободного падения
        dt = 1 / fps  # Диффиренциалл по времени (нужен для автоматической корриктировки точности просчета скорости
        # при изменении fps)

        # Да простит меня преподаватель, сопротивлением воздуха я пренебрегу, а то с тригонометрией возится - такое себе

        if keys[pg.K_SPACE] and self.isCollided['down']:
            self.isCollided['down'] = False
            self.current_speed['y'] = self.move_speed['y']
        else:  # если мы уже находимся в прыжке
            self.current_speed['y'] -= g * dt
            self.rect.y -= self.current_speed['y']

            if self.current_speed['y'] <= -300:  # из-за сопротивления воздуха человек не может падать быстрее
                self.current_speed['y'] = -300  # выставляем максимальную допустимую скорость падения

            check_collide = self.collided()

            if check_collide:
                if self.current_speed['y'] < 0:  # Если падаем
                    platforms = pg.sprite.spritecollide(self, self.level.platforms, dokill=False)
                    floor = pg.sprite.spritecollide(self, self.level.floor, dokill=False)
                    for platform in platforms:
                        # print(platform)
                        # print(platform.rect.top, self.rect.bottom)
                        if platform.rect.top + 10 > self.rect.bottom >= platform.rect.top:
                            self.current_speed['y'] = 0
                            self.isCollided['down'] = True
                            self.rect.y += platform.rect.top - self.rect.bottom
                            break
                    for floor_tile in floor:
                        if floor_tile.rect.top < self.rect.bottom < floor_tile.rect.top + 10:
                            self.current_speed['y'] = 0
                            self.isCollided['down'] = True
                            self.rect.y += floor_tile.rect.top - self.rect.bottom
                            break
                if self.current_speed['y'] > 0:
                    celling = pg.sprite.spritecollide(self, self.level.celling, dokill=False)
                    for celling_tile in celling:
                        if celling_tile.rect.bottom - 10 < self.rect.top <= celling_tile.rect.bottom:
                            self.current_speed['y'] = 0
                            self.rect.top += celling_tile.rect.bottom - self.rect.top

            # if self.current_speed['y'] < 0 and collide_check[0]:
            #     self.current_speed['y'] = 0
            #     self.rect.bottom += self.level.level.sprites()[collide_check[1]].rect.top - self.rect.bottom
            #     self.is_jump = False

            if self.rect.bottom >= WIN_height:  # Здесь седовало бы проверять, стоит ли персонаж, но поскольку
                # платформ нет, то проверяю столкновение с полом. этот метод будет не применим во время самой игры
                self.rect.y += WIN_height - self.rect.bottom
                self.is_jump = False

    def set_level(self, level: pg.sprite.Group):
        self.level = level

    def collided(self):
        """
        Втолкнулся ли герой с тайлом уровня
        :return: массив из булева значения и индекса объекта, с которым произошло столкновение
        """
        index = self.rect.collidelist(self.level.level.sprites())
        return index != -1


def main():
    display = pg.display.set_mode((WIN_width, WIN_height))
    clock = pg.time.Clock()
    hero = Hero()
    while 1:
        display.fill([255] * 3)

        hero.update(display)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        pg.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()

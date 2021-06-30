import pygame as pg

WIN_width = 1000
WIN_height = 500

fps = 60


class Hero(pg.sprite.Sprite):

    def __init__(self, x, y):
        # ща буит куча переменных, поэтому держись
        # Необходимые для анимации переменные
        self.hp = 10 # хп героя
        self.mana = 100  # мана героя
        self.facing = 0  # 0 - налево, 1 - направо
        self.animation = {  # Тут собраны все анимации, доступные герою
            'walk': [pg.image.load(f'Animations/Hero/Walk/L{frame}.png') for frame in range(1, 9)]  # ходьба
        }
        self.walk_state = 1  # то, в каком положении сейчас находится гг
        # Переменные для передвижения
        self.move_speed = {  # то, с какой скоростью герой может двигаться
            'x': 5,  # с какой скоростью герой бегает
            'y': 8  # с какой силой герой прыгает
        }
        self.current_speed = {  # текущая скорость по передвижения персонажа
            'x': 0,
            'y': 0
        }

        # self.is_jump = False  # Находится ли персонаж в прыжке
        # обязательные переменные
        pg.sprite.Sprite.__init__(self)  # Это необходимо для корректной работы класса
        self.image = self.animation['walk'][0]  # Пока поставим первое изображение ходьбы в качестве спокойствия
        # self.image = self.image.subsurface((20, 20, 50, 80))
        # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.subsurface
        self.rect = self.image.get_rect(x=x, y=y)  # располагаем героя в определенной точке пространства
        self.level = None
        # Лямбда, которая проверяет, может ли герой столкнуться телом с препятствием
        self.intersection = lambda y1, y2, l1, l2: (y1 - y2) + l2 >= 0 if (y1 - y2) > 0 else (y1 - y2) + l1 >= 0
        # Упирается ли герой во что-то
        self.isCollided = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.bullets = pg.sprite.Group()  # все снаряды, которые выпустил герой

    def update(self, surface: pg.surface.Surface, level=None, events: pg.event.get() = None):
        self.check_controls(events=events)  # Проверяем управление
        self.image = self.get_frame()  # просчитываем кадр анимации
        self.bullets.update()  # Обновляем все пули в группе
        self.bullets.draw(surface)  # отрисовываем пули
        self.draw(surface, self.image)  # Рисуем героя на экране

    def draw(self, surface: pg.surface.Surface, image):  # Отрисовать героя на экране

        surface.blit(self.image, self.rect)

    def get_frame(self):  # Узнаем, на каком кадре находится анимация
        frame = int((self.walk_state // 3) % len(self.animation['walk']))  # при каждом передвижении мы немного
        # увеличиваем переменную self.walkstate
        return pg.transform.flip(self.animation['walk'][frame], bool(self.facing), False)

    def check_controls(self, events: pg.event.get() = None):  # events нужен, так как pygame крайне не любит, когда
        # много раз вызывают pg.event.get(), но ее можно не передавать, если персонаж не должен атаковать
        """
        Изменяет координаты пероснажа, а также помогает с рассчетом анимации
        :return: Конкретное изображение из анимации героя
        """
        keys = pg.key.get_pressed()

        if keys[pg.K_d]:  # вправо
            self.current_speed['x'] = self.move_speed['x']
            self.facing = 1  # поворачиваем героя лицом вправо
            self.walk_state += 1 / 3  # продвигаем анимацию
            walls = pg.sprite.spritecollide(self, self.level.walls_left, dokill=False)  # все стены, с которыми
            # столкнулся гг
            for wall in walls:
                if self.intersection(self.rect.y, wall.rect.y, self.rect.h, wall.rect.h):  # если гг может в них
                    # впилиться телом
                    self.current_speed['x'] = 0  # Останавливаемся

        elif keys[pg.K_a]:  # Влево
            self.current_speed['x'] = self.move_speed['x'] * -1  # задаем скорость (предварительно
            self.facing = 0  # поворачиваемся Влево
            self.walk_state += 1 / 3  # Продвигает анимацию
            walls = pg.sprite.spritecollide(self, self.level.walls_right, dokill=False)  # стены, с которыми мы
                                                                                            # столкнулись
            for wall in walls:
                if self.intersection(self.rect.y, wall.rect.y, self.rect.h, wall.rect.h):  # можем ли мы напороться
                                                                                            # на это пузом
                    self.current_speed['x'] = 0  # Если можем, то останавливаемся


        else:  # если мы вообще не нажали кнопку
            self.current_speed['x'] = 0
            self.walk_state = 1

        self.checkAttack(events)  # Проверяем атаку
        self.check_gravity(keys)  # Проверяем состояние прыжка

        self.rect.x += self.current_speed['x']

    def checkAttack(self, events: pg.event.get()):
        # Если персонаж может атаковать
        if events is not None:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.bullets.add(Bullet('Animations/Hero/Bullets/bullet1.png', self.facing, self.rect.center))
        pg.sprite.groupcollide(self.bullets, self.level.level, True, False)

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
                self.isCollided['down'] = True

    def set_level(self, level: pg.sprite.Group):
        self.level = level

    def collided(self):
        """
        Втолкнулся ли герой с тайлом уровня
        :return: массив из булева значения и индекса объекта, с которым произошло столкновение
        """
        index = self.rect.collidelist(self.level.level.sprites())
        return index != -1


class Bullet(pg.sprite.Sprite):
    def __init__(self, img_src: str, direction, startPos):
        super().__init__()
        img = pg.image.load(img_src)  # анимации нет, поэтому можно так загрузить картинку
        img = img.subsurface((0, 500, 1280, 280))
        self.direction = not direction  # так как пуля изначально смотрит вправо, мы немного схалтурим
        self.image = pg.transform.flip(pg.transform.scale(img, [13, 5]), self.direction, 0)
        self.rect = self.image.get_rect()
        self.rect.center = startPos
        self.speed = 10  # скорость по х

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self.speed * (1 if self.direction == 0 else -1)


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

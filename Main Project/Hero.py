import pygame as pg

WIN_width = 1000
WIN_height = 500

fps = 60


class Hero(pg.sprite.Sprite):

    def __init__(self):
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
        self.rect = self.image.get_rect()
        self.level = None

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
        if keys[pg.K_a]:
            self.current_speed['x'] = self.move_speed['x'] * (-1)
            self.facing = 0
            self.walk_state += 1 / 3
        elif keys[pg.K_d]:
            self.current_speed['x'] = self.move_speed['x']
            self.facing = 1
            self.walk_state += 1 / 3
        else:
            self.current_speed['x'] = 0
            self.walk_state = 1
        self.check_jump(keys)  # Проверяем состояние прыжка
        self.rect.x += self.current_speed['x']

    def check_jump(self, keys):
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

        if keys[pg.K_SPACE] and not self.is_jump:
            self.is_jump = True
            self.current_speed['y'] = self.move_speed['y']
        else:  # если мы уже находимся в прыжке
            self.current_speed['y'] -= g * dt
            self.rect.y -= self.current_speed['y']

            if self.current_speed['y'] <= -300:  # из-за сопротивления воздуха человек не может падать быстрее
                self.current_speed['y'] = -300  # выставляем максимальную допустимую скорость падения

            collide_check = self.check_collision()

            if collide_check[0]:
                if self.current_speed['y'] > 0:
                    index = self.rect.collidelist(self.level.celling.sprites())
                    if index != -1:
                        self.current_speed['y'] = 0

                if self.current_speed['y'] < 0:
                    platform_index = self.rect.collidelist(self.level.platforms.sprites())
                    platform_rect = self.level.platforms.sprites()[platform_index].rect
                    floor_index = self.rect.collidelist(self.level.floor.sprites())
                    floor_rect = self.level.floor.sprites()[floor_index].rect
                    if platform_index != -1 and platform_rect.top <= self.rect.bottom < platform_rect.bottom:
                        self.current_speed['y'] = 0
                        # self.rect.y -= self.rect.bottom - floor_rect.top
                        self.is_jump = False
                    if floor_index != -1 and floor_rect.top - 1 <= self.rect.bottom < floor_rect.top + 10:
                        self.current_speed['y'] = 0
                        self.is_jump = False

                if self.current_speed['x'] != 0:
                    wall_index = self.rect.collidelist(self.level.walls.sprites())
                    wall_rect = self.level.walls.sprites()[wall_index].rect
                    if wall_index != -1:
                        if self.rect.x <= wall_rect.right or self.rect.right >= wall_rect.left:
                            self.current_speed['x'] = 0


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

    def check_collision(self):
        """
        Втолкнулся ли герой с тайлом уровня
        :return: массив из булева значения и индекса объекта, с которым произошло столкновение
        """
        index = self.rect.collidelist(self.level.level.sprites())
        return [index != -1, index]


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

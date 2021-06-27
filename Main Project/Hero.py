import pygame as pg

WIN_width = 1000
WIN_height = 700

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
            'y': 10  # с какой силой герой прыгает
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

    def update(self, surface: pg.surface.Surface, level=None):
        self.check_controls()
        self.image = self.get_frame()
        self.draw(surface, self.image)

    def draw(self, surface: pg.surface.Surface, image):

        surface.blit(self.image, self.rect)

    def get_frame(self):
        frame = int((self.walk_state // 3) % len(self.animation['walk']))
        return pg.transform.flip(self.animation['walk'][frame], self.facing, 0)

    def check_controls(self):
        """
        Изменяет координаты пероснажа, а также рассчитывает его анимацию
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
        self.check_jump(keys)
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

        # Очень длинно проверяем, не нажат ли пробел
        if keys[pg.K_SPACE] and not self.is_jump:
            self.is_jump = True
            self.current_speed['y'] = self.move_speed['y']
        else:  # если мы уже находимся в прыжке
            self.current_speed['y'] -= g * dt
            self.rect.y -= self.current_speed['y']

            if self.current_speed['y'] <= -300:  # из-за сопротивления воздуха человек не может падать быстрее
                self.current_speed['y'] = -300  # выставляем максимальную допустимую скорость падения

            if self.rect.bottom >= WIN_height:  # Здесь седовало бы проверять, стоит ли персонаж, но поскольку
                # платформ нет, то проверяю столкновение с полом
                self.rect.y += WIN_height - self.rect.bottom
                self.is_jump = False


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

import pygame as pg

WIN_width = 1000
WIN_height = 500

FPS = 60
GRAVITY = 10 / FPS


class Hero(pg.sprite.Sprite):
    MAX_HP = 100
    MAX_MANA = 100
    MANA_FOR_SPELL = 15

    def __init__(self, x, y):
        # ща буит куча переменных, поэтому держись
        # Необходимые для анимации переменные
        self.hp = Hero.MAX_HP  # хп героя
        self.mana = Hero.MAX_MANA  # мана героя
        self.facing = 0  # 0 - налево, 1 - направо
        self.animations = {  # Тут собраны все анимации, доступные герою
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
        self.image = self.animations['walk'][0]  # Пока поставим первое изображение ходьбы в качестве спокойствия
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
        keys = pg.key.get_pressed()
        self.check_controls(keys, events)  # Проверяем управление

        # костылим гравитацию
        if not self.isCollided['down']:
            self.current_speed['y'] += GRAVITY

        self.isCollided['down'] = False  # заново проверяем, стоим ли мы
        self.rect.y += self.current_speed['y']
        self.checkCollide_y()
        self.rect.x += self.current_speed['x']
        self.checkCollide_x()

        self.animation()
        self.draw(surface)

    def draw(self, surface: pg.surface.Surface):  # Отрисовать героя на экране

        surface.blit(pg.transform.flip(self.image, bool(self.facing), 0), self.rect)

    def get_frame(self):  # Узнаем, на каком кадре находится анимация
        frame = int((self.walk_state // 3) % len(self.animations['walk']))  # при каждом передвижении мы немного
        # увеличиваем переменную self.walkstate
        return pg.transform.flip(self.animations['walk'][frame], bool(self.facing), False)

    def check_controls(self, keys, events=None):  # events нужен, так как pygame крайне не любит, когда
        # много раз вызывают pg.event.get(), но ее можно не передавать, если персонаж не должен атаковать
        """
        Изменяет скорости пероснажа, а также помогает с рассчетом анимации
        :return: None
        """
        if keys[pg.K_a]:
            self.current_speed['x'] = self.move_speed['x'] * -1
        if keys[pg.K_d]:
            self.current_speed['x'] = self.move_speed['x']
        if not keys[pg.K_a] and not keys[pg.K_d]:
            self.current_speed['x'] = 0
        if keys[pg.K_SPACE] and self.isCollided['down']:
            self.current_speed['y'] = self.move_speed['y'] * -1
        self.checkAttack(events)

    def checkAttack(self, events: pg.event.get()):
        # Если персонаж может атаковать
        if events is not None:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.consume_mana(Hero.MANA_FOR_SPELL):
                    self.bullets.add(Bullet('Animations/Hero/Bullets/bullet1.png', self.facing, self.rect.center))
        pg.sprite.groupcollide(self.bullets, self.level.level, True, False)

    def checkCollide_y(self):

        for tile in self.level.level:

            if pg.sprite.collide_rect(self, tile):

                if self.current_speed['y'] > 0:  # Если падаем
                    if self.rect.bottom < tile.rect.top + 10:  # Если падаем на плитку сверху
                        self.rect.bottom = tile.rect.top  # становимся на плитку
                        self.isCollided['down'] = True  # понимаем, что мы стоим
                        self.current_speed['y'] = 0  # перестаем падать

                elif self.current_speed['y'] < 0:  # если движемся вверх
                    if tile not in self.level.platforms \
                            and self.rect.top > tile.rect.bottom - 10:
                        self.current_speed['y'] = 0
                        self.rect.top = tile.rect.bottom

    def checkCollide_x(self):
        for tile in self.level.level:
            if pg.sprite.collide_rect(self, tile) and tile not in self.level.platforms:

                if self.current_speed['x'] < 0:  # Влево
                    self.rect.left = tile.rect.right
                    self.current_speed['x'] = 0
                elif self.current_speed['x'] > 0:  # Вправо
                    self.rect.right = tile.rect.left
                    self.current_speed['x'] = 0

    def set_level(self, level: pg.sprite.Group):
        self.level = level

    def animation(self):
        if self.current_speed['x'] < 0:  # Влево
            self.facing = 0
        elif self.current_speed['x'] > 0:  # Вправо
            self.facing = 1

    def collided(self):
        """
        Втолкнулся ли герой с тайлом уровня
        :return: массив из булева значения и индекса объекта, с которым произошло столкновение
        """
        index = self.rect.collidelist(self.level.level.sprites())
        return index != -1

    def heal(self, hp):
        self.hp += hp
        if self.hp > Hero.MAX_HP:
            self.hp = Hero.MAX_HP

    def restore_mana(self, mana):
        self.mana += mana
        if self.mana > Hero.MAX_MANA:
            self.mana = Hero.MAX_MANA

    def get_hp(self):
        return self.hp

    def get_mana(self):
        return self.mana

    def death(self):
        pass

    def consume_mana(self, mana):
        if self.mana >= mana:
            self.mana -= mana
            return True
        return False

    def damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.death()


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
        clock.tick(FPS)


if __name__ == '__main__':
    main()

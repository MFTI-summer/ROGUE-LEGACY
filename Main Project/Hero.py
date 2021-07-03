import pygame as pg
import Enemy
from math import ceil

pg.init()
pg.mixer.init()

WIN_width = 1000
WIN_height = 500

FPS = 60
GRAVITY = 12.4 / FPS


class Hero(pg.sprite.Sprite):
    MAX_HP = 100
    MAX_MANA = 100
    MANA_FOR_SPELL = 15

    def __init__(self, x, y):
        self.dframe = {
            'jump': 1 / 20,
            'walk': 1 / 7,
            'attack': 1 / 5
        }  # скорость смены кадров
        self.weaponRect = None
        self.swordDamage = 34
        self.walk_or_collide = pg.mixer.Sound('Sounds/Sound_collide_and_walk.wav')
        self.shut = pg.mixer.Sound('Sounds/Shut.wav')
        self.hit = pg.mixer.Sound('Sounds/Sound_Hit_Hero.ogg')
        self.can_play = True
        # ща буит куча переменных, поэтому держись
        # Необходимые для анимации переменные
        self.current_level = 6
        self.jumpDown = False  # Должны ли мы спрыгнуть вниз
        self.onPlatform = False  # Стоим ли мы на полупрозрачной платформе
        self.hp = Hero.MAX_HP  # хп героя
        self.mana = Hero.MAX_MANA  # мана героя
        self.facing = 0  # 0 - направо, 1 - налево
        self.animations = {  # Тут собраны все анимации, доступные герою
            'walk': [(pg.image.load(f'Animations/Hero/New animation/Walk/R{frame}.png')) for frame in range(1, 4 + 1)],
            'jump': [pg.image.load(f'Animations/Hero/New animation/Jump/J{frame}.png') for frame in range(1, 2 + 1)],
            'fall': [pg.image.load('Animations/Hero/New animation/Fall/F.png')],
            'attack': [pg.image.load(f'Animations/Hero/New animation/Attack/A{frame}.png') for frame in
                       range(1, 3 + 1)],
            'count': 0
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
        self.weapon = pg.sprite.GroupSingle()
        # self.image = self.image.subsurface((20, 20, 50, 80))
        # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.subsurface
        self.rect = self.image.get_rect(x=x, y=y)  # располагаем героя в определенной точке пространства
        self.level = None
        self.currentAnimation = 'walk'
        # Упирается ли герой во что-то
        self.isCollided = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.bullets = pg.sprite.Group()  # все снаряды, которые выпустил герой
        self.bulletDamage = 40  # Урон от пуль
        self.immortalTime = {
            'max': 1 * FPS,
            'current': 0
        }  # время бессмертия после урона в кадрах

        self.attackProperties = dict(isAttacking=False, attackState=0, attackMaxLength=0.2 * FPS, couldown = 1*FPS)
        self.isAlive=True


    def update(self, surface: pg.surface.Surface, level=None, events: pg.event.get() = None):
        print("*"*20)

        keys = pg.key.get_pressed()
        self.check_controls(keys, events)  # Проверяем управление

        print ("self.isCollided['down']", self.isCollided['down'])
        # костылим гравитацию
        # if not self.isCollided['down']:
        self.current_speed['y'] += GRAVITY

        self.isCollided['down'] = False  # заново проверяем, стоим ли мы

        print("round(self.current_speed['y'])  ", self.current_speed['y'], ceil(self.current_speed['y']))

        self.rect.y += ceil(self.current_speed['y'])
        self.checkCollide_y()
        print ("self.isCollided['down']", self.isCollided['down'])

        self.rect.x += self.current_speed['x']
        self.checkCollide_x()
        # Делаем анимацию
        self.animation()
        self.check_damage()
        self.bullets.update()
        self.bullets.draw(surface)
        self.weapon.update(surface)
        # Рисуем все
        self.draw(surface)

    def draw(self, surface: pg.surface.Surface):  # Отрисовать героя на экране

        surface.blit(pg.transform.flip(self.image, bool(self.facing), 0), self.rect)

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

        if keys[pg.K_s]:
            self.jumpDown = True
        self.jump(keys, events)
        self.checkAttack(events)

    def jump(self, keys, events):
        if events is not None: # if events != []
            if keys[pg.K_SPACE] and self.isCollided['down']:
                self.current_speed['y'] = self.move_speed['y'] * -1
                self.animations['count'] = 0
            for event in events:
                if event.type == pg.KEYDOWN and event.key == pg.K_s:  # Спрыгнуть вниз c платформы
                    self.jumpDown = True

    def checkAttack(self, events: pg.event.get()):
        # Если персонаж может атаковать
        if events is not None:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3 and self.consume_mana(Hero.MANA_FOR_SPELL):  # стреляем
                        self.bullets.add(Bullet('Animations/Hero/Bullets/bullet1.png', self.facing, self.rect.center))
                    if event.button == 1:  # Атакуем "мечом", меча пока нет
                        self.meleeAttack()  # TODO: добавить анимацию удара
        if self.attackProperties['isAttacking']:
            self.meleeAttack()

        pg.sprite.groupcollide(self.bullets, self.level.level, True, False)
        bullet_damaged_mobs = pg.sprite.groupcollide(self.bullets, self.level.mobs, 1, 0)
        if len(bullet_damaged_mobs) > 0:
            self.damage_mobs(bulletDamaged=bullet_damaged_mobs)

    def damage_mobs(self, bulletDamaged: dict = None, swordDamaged=None):
        if bulletDamaged is not None:
            for mob in bulletDamaged.values():
                if type(mob[0]) is not Enemy.Ghost:
                    mob[0].get_damage(self.bulletDamage)
                    print(mob[0].health)

    def check_damage(self):
        sprite = pg.sprite.spritecollideany(self, self.level.mobs)
        if sprite is not None:
            if self.immortalTime['current'] == 0:
                self.get_damage(sprite.damage)
                self.immortalTime['current'] = 1
        if self.immortalTime['current'] > 0:
            self.immortalTime['current'] += 1
            if self.immortalTime['current'] >= self.immortalTime['max']:
                self.immortalTime['current'] = 0

    def meleeAttack(self):
        # Пока мы просто создаем прямоугольник, внутри которого враги получают урон
        # attackField = pg.rect.Rect(self.rect.x + (self.rect.w * self.facing), self.rect.y, 20, self.rect.h)
        if not self.attackProperties['isAttacking']:
            left = self.rect.x + self.rect.w if self.facing is 0 else self.rect.x - self.rect.w
            top = self.rect.y
            width = 30
            height = self.rect.h
            self.weaponRect = pg.rect.Rect(left, top, width, height)
            self.attackProperties['isAttacking'] = True
            self.animations['count'] = 0
        else:
            self.attackProperties['attackState'] += 1
            if self.attackProperties['attackState'] == self.attackProperties['attackMaxLength']:
                self.attackProperties['attackState'] = False
                self.attackProperties['isAttacking'] = False
        mobRects = {mob: mob.rect for mob in self.level.mobs}
        for mob in mobRects:
            print(mob)
            if self.weaponRect.colliderect(mobRects[mob]):
                mob.get_damage(self.swordDamage)
                print('hp -', mob.health)

    def checkCollide_y(self):  # TODO: добавить возможность спрыгнуть с платформы

        print("CollideAny",pg.sprite.spritecollideany(self, self.level.level, collided = None))
        print(f"rect.y {self.rect.y}, bottom {self.rect.bottom}, speed {self.current_speed['y']}")

        for tile in self.level.level:

            if tile.rect.colliderect(self.rect):
                print(f"203 строка =={self.rect.bottom}=={tile.rect.top}==={self.current_speed['y']}==========================")

                if self.current_speed['y'] > 0:  # Если падаем
                    if self.rect.bottom < tile.rect.top + 15:  # Если падаем на плитку сверху
                        if tile in self.level.platforms and self.jumpDown:
                            pass
                        else:
                            self.rect.bottom = tile.rect.top  # становимся на плитку
                            self.current_speed['y'] = 0  # перестаем падать
                            self.isCollided['down'] = True
                            self.jumpDown = False
                    else:
                        self.jumpDown = False  # Если мы уже упали с платформы

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

    def check_correct_level(self):

        if -20 < self.rect.x < 720 and 0 < self.rect.y < 500:
            return False

        return True

    def change_level(self, level: pg.sprite.Group, side):
        if side == "right":
            self.rect.x -= 720
            self.level = level
        elif side == "left":
            self.rect.x += 720
            self.level = level
        elif side == "down":
            self.rect.y -= 500
            self.level = level
        elif side == "up":
            self.rect.y += 500
            self.level = level

    def animation(self):
        print ('\n', self.current_speed['y'])
        print (self.isCollided['down'])
        if self.current_speed['y'] != 0 and not self.isCollided['down']:
            if self.current_speed['y'] < 0:  # Если подлетаем
                self.currentAnimation = 'jump'
                self.animations['count'] += self.dframe['jump']
                print(self.animations['count'])
            elif self.current_speed['y'] > 0:  # Если падаем
                self.currentAnimation = 'fall'
        else:
            if self.current_speed['x'] < 0:  # Если идем влево
                self.facing = 1  # Разворачиваем
                self.animations['count'] += self.dframe['walk']

            elif self.current_speed['x'] > 0:  # Вправо
                self.facing = 0
                self.animations['count'] += self.dframe['walk']

            if self.current_speed['x'] !=0:
                self.currentAnimation = 'walk'
            else:
                pass
                ## TODO добавить картинку стояния на месте

        if self.attackProperties['isAttacking']:
            self.currentAnimation = 'attack'
            self.animations['count'] += self.dframe['attack']
        self.set_frame()
        print(self.animations['count'])

    def set_frame(self):  # Узнаем, на каком кадре находится анимация
        frame = int((self.animations['count'] // 1) % len(self.animations[self.currentAnimation]))
        print(frame)
        print(self.currentAnimation)
        self.image = self.animations[self.currentAnimation][frame]

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
        self.isAlive=False
        print("YOU ARE DEAD")

    def consume_mana(self, mana):
        if self.mana >= mana:
            self.mana -= mana
            return True
        return False

    def get_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.death()

    def sounds(self):
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_a or e.key == pg.K_d:
                    self.walk_or_collide.play()
        for tile in self.level.level:
            if self.rect.bottom < tile.rect.top + 10 and self.can_play == True:
                if self.rect.bottom > tile.rect.bottom - 10:
                    self.walk_or_collide.play()
                    if self.current_speed['y'] == 0:
                        if self.rect.top == tile.rect.bottom:
                            self.can_play = True
                        else:
                            self.can_play = False

                        break


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

    def update(self) -> None:
        self.rect.x += self.speed * (-1 if self.direction == 0 else 1)


class Sword(pg.sprite.Sprite):
    def __init__(self, start_pos, *groups):
        super().__init__(*groups)
        temporal_image = pg.image.load('Animations/Hero/Sword/sword.png')  # Пока сам меч не анимируется как картинка
        temporal_image = pg.transform.rotate(temporal_image, 45)
        self.image = pg.transform.scale(temporal_image, (60, 60)).convert_alpha()
        # self.image.set_colorkey([255] * 3)
        self.rot_image = self.image.copy()
        self.rect = self.image.get_rect(center=start_pos)
        self.rot_rect = self.rect.copy()

        self.anim_properties = {
            'length': 0.5 * FPS,  # Максимальная продолжительность атаки
            'currentState': 0,  # Сколько времени с момента начала атаки уже прошло (в кадрах)
            'angleSpeed': -180 / FPS  # Возможно пригодится для анимации меча
        }

    def update(self, surface):
        if self.anim_properties['currentState'] <= self.anim_properties['length']:
            self.animation()
            self.draw(surface)
        else:
            self.kill()

    def animation(self):
        self.anim_properties['currentState'] += 1

        self.rot_image = pg.transform.rotate(self.image, self.anim_properties['currentState'])
        self.rot_rect.center = self.rect.center

    def draw(self, surface: pg.surface.Surface):
        surface.blit(self.rot_image, self.rot_rect)


def main():
    display = pg.display.set_mode((WIN_width, WIN_height))
    clock = pg.time.Clock()
    hero = Hero(100, 100)
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

import pygame as pg

# ПРОЧИТАЙ, ВАЖНО!!! Как тут оставить документацию к пакету? А, да пофиг, просто коммент захреначу. Чтобы работать с
# этим модулем, тебе лучше ознакомиться с исходным кодом Вот тебе кратенко обо всем, что тут происходит. Во-первых,
# я писал комментарии второпях и в них наверняка есть ошибки, но мне пофиг Во-вторых, если ты запустишь файл,
# то не увидишь ничего хорошего, сейчас поясню почему так На самом деле этот файл содержит генератор уровня из плиток
# (я решил, что для создания однотипных уровней это пойдет) можно поставить любые текстурки, точно также можно
# спокойно расширить набор плиток для уровней. Все это делается в параметре tiles_dict класса Level. Вообще этот
# словарь можно было бы вынести в независимую переменную, но мне приятнее видеть ее как непосредственный атрибут
# класса. По сути генератор просто перебирает все символы в "карте" уровня (читай: многострочной строке ). Примером
# этого является переменная test_map рекомендую ее тоже глянуть, чтобы понять, что тут и как. Далее алгоритм
# заменяет место символа на плитку  с определенной текстуркой, но по строго определенными правилам. К примеру,
# все плитки должны иметь одинаковые размеры, пикселем больше или пикселем меньше, и все несется к чертям. Все плитки
# должны быть квадратными. Их, по-идее можно сделать любой прямоугольной формы, но тогда код надо будет допилить.
# Если такое необходимо, пишите мне, соображу что-нибудь, ну или скажу "да пошли вы", тут уж на какое настроение
# попадешь Все остальное есть в комментариях, поэтому не стесьняйся их читать. Ну и так же лучше все же понимать
# что-то в программировании.


# Эти переменные мне нужны чисто сейчас. Далее они тебе не понядобятся
WIN_width: int = 1000
WIN_height: int = 700
# Та сама карта-пример, про которую я говорил в комментарии
test_map = \
    """
.~~~~~~~~~~~~~.
).............(
).............(
._\...........(
.~>...........(
)........./___.
).........<~~~.
).............(
).............(
._____________.
"""  # row == 15, col = 10  Это просто размеры, которые я пометил для себя.


# Очень важно, чтобы кол-во символов в ряду совпадало (хотя генератор от этого не сломается
# но выглядеть будет лучше. Точки обозначают пустое место, поэтому можно все дозаполнить ими


class Level:  # Тот самый класс, ради которого писался весь код
    # Тут размещается словарь с символами и значениями, которые этим символам присваиваются
    # Сюда можно добавить любую другую картинку и приписать ей значение
    # В качестве значения подойдет любой символ, который еще не использовался и котрый можно набрать на клаве
    tiles_dict = {
        '.': None,
        '/': ['Textures/Outer_corner.png', 0],
        '\\': ['Textures/Outer_corner.png', -90],
        '<': ['Textures/Outer_corner.png', 90],
        '>': ['Textures/Outer_corner.png', 180],
        '_': ['Textures/Block.png', 0],
        '(': ['Textures/Block.png', 90],
        ')': ['Textures/Block.png', -90],
        '~': ['Textures/Block.png', 180]
    }

    def __init__(self, level_map):  # self.step нужен, чтобы определить размер шага, потом увидишь где это понадобится
        self.step = Tile.size
        self.level = None
        self.generate_level(level_map)

    def generate_level(self, level_map: str):
        # это документация к функции, с ней тоже можно ознакомиться
        """
        Получает на вход "карту уровня", после чего генерирует уровень на ее основе
        :param level_map: карта, представляющая собой многострочную строку,
        содержащая специальные обозначения всех возможных тайлов
        :return: None
        """
        # Это группа спрайтов представляет собой все тайлы, которые есть на уровне.
        self.level = pg.sprite.Group()

        split_map = level_map.split('\n')  # Разделяем "карту" на отдельные слои

        # Иногда карта уровня будет содержать пустые слои, которые образуется от переноса строк в начале и в конце
        # в этом генераторе я отфильтровываю их
        # По идее можно было бы сделать все преобразоавния в одну строку,
        # но тогда пострадала бы читабельность кода
        layers = [layer for layer in split_map if layer != '']

        # это - начальное положение верхнего левого тайла
        x = 100
        y = 100

        # Теперь расставляем тайлы, соответствующие символам

        for layer in layers:
            # чтобы генератор постоянно возвращался на левый конец уровня и весь уровень не уезжал по горизонтали
            x = 100
            for symbol in layer:
                # Здесь мы получаем параметры плитки, на которую мы меняем символ в "карте"
                # (до сих пор язык не поворачивается называть это картой, но по функциям - так и есть
                tile_properties = self.tiles_dict[symbol]  # В переменную мы записываем список из двух значений
                # 1. путь к изображению
                # 2. градус, под которым его надо повернуть
                # впрочем, ты можешь это знать, если решил почитать tiles_dict
                if tile_properties is None:
                    # Поскольку точке не присвоено никакого тайла, то выполнять дальнейшие действия бессмысленно
                    # Поэтому мы просто пропускаем все остальные действия (едиственно, что мы все же продвигаем
                    # генератор дальше)
                    x += self.step
                    continue
                src = tile_properties[0]  # путь к изображению
                degree = tile_properties[1]  # Градус будущего поворота
                self.level.add(Tile(src, degree, x, y))  # добавляем новую плитку к уже имеющимся
                x += self.step  # смещаемся вправо на ширину одной плитки
            y += self.step  # спускаемся вниз

    def update(self, surface):
        """
        Если что-то изменилось, следует обновить весь уровень
        :param surface:
        :return:
        """
        # self.observe(surface) - тут я хотел сделать движения камеры, но не срослось
        self.level.update(surface)  # Обновляем все тайлы

    def observe(self, surface):  # тут я хотел реализовать функции камеры, но, как ты уже знаешь, не получилось
        for sprite in self.level:
            sprite.update(surface)


class Tile(pg.sprite.Sprite):
    size = 50

    def __init__(self, img_file_src: str, degree, x, y):
        pg.sprite.Sprite.__init__(self)
        image = pg.image.load(img_file_src).convert()
        self.rect = image.get_rect()
        self.image = pg.transform.rotate(image, degree)
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self, surface: pg.surface.Surface, *args, **kwargs) -> None:
        """
        тут мы обновляем положение плиточек
        :param surface:
        PyCharm добавил еще два параметра, но мне лень их стирать, да и
        работе метода они никак не мешают
        :param args:
        :param kwargs:
        :return:
        """
        surface.blit(self.image, self.rect)  # тут все понятно

    def move(self):  # Тут я пытался заставить плитки двигаться, но не получилось
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.y += self.speed
        if keys[pg.K_s]:
            self.y -= self.speed
        if keys[pg.K_a]:
            self.y += self.speed
        if keys[pg.K_d]:
            self.y -= self.speed
        self.update()


def main():  # Если модуль все же запустили как приложение, то выполняется простенькая программа
    # Думаю, что пояснений к ней не требуется
    sc = pg.display.set_mode((WIN_width, WIN_height))
    sc.fill
    generator = Level(test_map)
    generator.update(sc)
    while 1:

        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
        pg.display.update()


if __name__ == '__main__':  # эта штука нужна, чтобы программа не запускалась при импорте
    main()

# В этом модуле куча багов и недоработок, но я все же выложу его
# эти ошибки не критичны, а если что-то станет необходимо, то
# всегда можно допилить без вреда для здоровья

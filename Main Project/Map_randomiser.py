import pygame as pg
import random
# Это символы, из которых может состоять карта.
available_characters = '.=_-I|><#№(){}[]'

level_map = [[], [], [], [], [], [], [], [], [], []]

# Функция только для откладки
def print_level_map():
    for i in range(0, row):
        print(''.join(level_map[i]))
    print(' ')

# Размеры карты
row = 10
col = 15

# Генерируем двумерный массив, в виде которого сначала будет храниться карта
# В нём не хватает четырёх "рядов" - их я позже добавлю в виде точек, т. к. иначе у персонажа не будет
# достаточно места для передвижения(точка означает пустое мето)

# Составление карты из пустых мест и кирпичей без полоски
for i in range (0, row):
    for j in range (0, col):
        new_cell_index = random.randint(0, 1)
        new_cell = available_characters[new_cell_index]
        level_map[i].append(new_cell)
print_level_map()

# Чтобы уровни плавно переходили друг в друга
level_map[4][0] = '.'
level_map[5][0] = '.'
level_map[4][14] = '.'
level_map[5][14] = '.'

# Чтобы герой мог пройти из одного конца уровня в другой, проверяется, можно ли с данной плитки уйти вправо или вверх
# и если нет, то справа или сверху добавляется пустая клетка (т. е. точка)
for x in range (1, col):
    for y in range (5, 8):
        if x < 14 and level_map[y][x+1] != '.':
            level_map[y][x+1] = '.'
        if y < 4 and level_map[y+1][x] != '.':
            level_map[y+1][x] = '.'
        if y > 5 and level_map[y-1][x] != '.':
            level_map[y-1][x] = '.'
# Чтобы кирпичи не "висели в воздухе"
for x in range(0, col):
    for y in range(0, row):
        if 0 < x < 14 and 5 < y < 9 and level_map[y+1][x] == '.':
            if level_map[y][x-1] == '.' or level_map[y][x+1] == '.':
                level_map[y+1][x] = '='
        elif 0 < x < 14 and 0 < y < 3 and level_map[y-1][x] == '.':
            if level_map[y][x-1] == '.' or level_map[y][x+1] == '.':
                level_map[y-1][x] = '='
        elif x == 0 and 0 < y < 3 and level_map[y-1][x] == '.' and level_map[y][x+1] == '.':
            level_map[y-1][x] = '='
        elif x == 14 and 0 < y < 3 and level_map[y-1][x] == '.' and level_map[y][x-1] == '.':
            level_map[y-1][x] = '='
        elif x == 0 and 5 < y < 9 and level_map[y+1][x] == '.' and level_map[y][x+1] == '.':
            level_map[y+1][x] = '='
        elif x == 14 and 5 < y < 9 and level_map[y+1][x] == '.' and level_map[y][x-1] == '.':
            level_map[y+1][x] = '='
print_level_map()
# Чтобы у кирпичей была полоска, если это нужно
for x in range(0, col):
    for y in range(0, row):
        if level_map[y][x] != '.':
            # Эта проверка нужна, чтобы не появлялась ошибка 'list index out of range'
            if 0 < x < 14 and 0 < y < 9:
                if level_map[y+1][x] == '.':
                    level_map[y][x] = '_'
                if level_map[y-1][x] == '.':
                    level_map[y][x] = '-'
                if level_map[y-1][x] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '['
                if level_map[y][x-1] == '.':
                    level_map[y][x] = 'I'
                if level_map[y][x+1] == '.':
                    level_map[y][x] = '|'
                if level_map[y][x-1] == '.' and level_map[y][x+1] == '.':
                    level_map[y][x] = ']'
                if level_map[y][x-1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '<'
                if level_map[y][x+1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '>'
                if level_map[y][x-1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '#'
                if level_map[y][x+1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '№'
                if level_map[y][x+1] == '.' and level_map[y+1][x] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = ')'
                if level_map[y][x-1] == '.' and level_map[y+1][x] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '('
                if level_map[y][x+1] == '.' and level_map[y][x-1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '{'
                if level_map[y][x+1] == '.' and level_map[y][x-1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '}'
            elif x == 0 and 0 < y < 9:
                if level_map[y+1][x] == '.':
                    level_map[y][x] = '_'
                if level_map[y-1][x] == '.':
                    level_map[y][x] = '-'
                if level_map[y-1][x] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '['
                if level_map[y][x+1] == '.':
                    level_map[y][x] = '|'
                if level_map[y][x+1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '>'
                if level_map[y][x+1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '№'
                if level_map[y][x+1] == '.' and level_map[y+1][x] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '('
            elif x == 14 and 0 < y < 9:
                if level_map[y+1][x] == '.':
                    level_map[y][x] = '_'
                if level_map[y-1][x] == '.':
                    level_map[y][x] = '-'
                if level_map[y-1][x] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '['
                if level_map[y][x-1] == '.':
                    level_map[y][x] = 'I'
                if level_map[y][x-1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '<'
                if level_map[y][x-1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '#'
                if level_map[y][x-1] == '.' and level_map[y+1][x] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '('
            elif 0 < x < 14 and y == 0:
                if level_map[y+1][x] == '.':
                    level_map[y][x] = '_'
                if level_map[y-1][x] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '['
                if level_map[y][x-1] == '.':
                    level_map[y][x] = 'I'
                if level_map[y][x+1] == '.':
                    level_map[y][x] = '|'
                if level_map[y][x-1] == '.' and level_map[y][x+1] == '.':
                    level_map[y][x] = ']'
                if level_map[y][x-1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '#'
                if level_map[y][x+1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '№'
                if level_map[y][x+1] == '.' and level_map[y][x-1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '}'
            elif 0 < x < 14 and y == 9:
                if level_map[y-1][x] == '.':
                    level_map[y][x] = '-'
                if level_map[y][x-1] == '.':
                    level_map[y][x] = 'I'
                if level_map[y][x+1] == '.':
                    level_map[y][x] = '|'
                if level_map[y][x-1] == '.' and level_map[y][x+1] == '.':
                    level_map[y][x] = ']'
                if level_map[y][x-1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '<'
                if level_map[y][x+1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '>'
                    level_map[y][x] = '№'
                if level_map[y][x+1] == '.' and level_map[y][x-1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '{'
            elif x == 0 and y == 0:
                if level_map[y+1][x] == '.':
                    level_map[y][x] = '_'
                if level_map[y][x+1] == '.':
                    level_map[y][x] = '|'
                if level_map[y][x+1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '№'
            elif x == 14 and y == 9:
                if level_map[y-1][x] == '.':
                    level_map[y][x] = '-'
                if level_map[y][x-1] == '.':
                    level_map[y][x] = 'I'
                if level_map[y][x-1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '<'
            elif x == 0 and y == 9:
                if level_map[y-1][x] == '.':
                    level_map[y][x] = '-'
                if level_map[y][x+1] == '.':
                    level_map[y][x] = '|'
                if level_map[y][x+1] == '.' and level_map[y-1][x] == '.':
                    level_map[y][x] = '>'
            elif x == 14 and y == 0:
                if level_map[y+1][x] == '.':
                    level_map[y][x] = '_'
                if level_map[y][x-1] == '.':
                    level_map[y][x] = 'I'
                if level_map[y][x-1] == '.' and level_map[y+1][x] == '.':
                    level_map[y][x] = '#'
            
print_level_map()










































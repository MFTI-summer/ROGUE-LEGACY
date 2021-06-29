import random
def generate_map():
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

    # Составление карты из пустых мест и кирпичей без полоски
    for i in range (0, row):
        for j in range (0, col):
            new_cell_index = random.randint(0, 1)
            new_cell = available_characters[new_cell_index]
            level_map[i].append(new_cell)

    # Чтобы уровни плавно переходили друг в друга
    level_map[4][0] = '.'
    level_map[5][0] = '.'
    level_map[4][14] = '.'
    level_map[5][14] = '.'

    # Чтобы герой мог пройти из одного конца уровня в другой, проверяется, можно ли
    # с данной плитки попасть в на пустые плитки в конце уровня
    # и если нет, то справа или сверху добавляется пустая клетка (т. е. точка)
    for x in range (0, row):
        for y in range (4, 6):
            if x < 15 and level_map[y][x+1] != '.':
                level_map[y][x+1] = '.'
            if y < 4 and level_map[y+1][x] != '.':
                level_map[y+1][x] = '.'
            if y > 5 and level_map[y-1][x] != '.':
                level_map[y-1][x] = '.'
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
    for i in range(0, len(level_map)):
        level_map[i] = ''.join(level_map[i])+'\n'
    level_map = ''.join(level_map)            
    return level_map








































import pygame


class InventorySlot:
    def __init__(self, length, hero, type):
        self._length = length  # Максимальная вместимость слота
        self._buf = []  # Предметы в слоте
        self._hero = hero
        self._type = type  # Тип предмета

    def store_item(self, item):
        if self._type == item.get_type():
            if len(self._buf) < self._length:
                self._buf.append(item)
            else:
                raise Exception("NOT ENOUGH SPACE")
        else:
            raise Exception("TYPE OF ITEM IS NOT CORRECT")

    def use_item(self):
        if len(self._buf) > 0:
            self._buf.pop(0).use(self._hero)

    def get_number_of_stored_items(self):
        return len(self._buf)

    def get_max_inventory_load(self):
        return self._length


class Item(pygame.sprite.Sprite):
    def __init__(self, type, sprite_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self._type = type

    def get_type(self):
        return self._type


class RestoreManaItem(Item):
    def __init__(self, mana, x, y):
        super().__init__("MANA", "Textures/mana potion.png", x, y)
        self._mana = mana

    def use(self, hero):
        hero.restore_mana(self._mana)


class HealItem(Item):
    def __init__(self, heal, x, y):
        super().__init__("HP", "Textures/healing salve.png", x, y)
        self._heal = heal  # Сколько восстановит

    def use(self, hero):
        hero.heal(self._heal)

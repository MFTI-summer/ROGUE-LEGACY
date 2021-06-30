import pygame.sprite


class InventorySlot(pygame.sprite.Sprite):
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

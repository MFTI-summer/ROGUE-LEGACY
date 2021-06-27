class InventorySlot:
    def __init__(self, length, hero, type):
        self._length = length
        self._buf = []
        self._hero = hero
        self._type = type

    def store_item(self, item):
        if self._type == item.type:
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


class Item:
    def __init__(self, type):
        self._type = type


class RestoreManaItem(Item):
    def __init__(self, mana):
        super().__init__("MANA")
        self._mana = mana

    def use(self, hero):
        hero.restore_mana(self._mana)


class HealItem(Item):
    def __init__(self, heal):
        super().__init__("HP")
        self._heal = heal

    def use(self, hero):
        hero.heal(self._heal)



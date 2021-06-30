import pygame


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

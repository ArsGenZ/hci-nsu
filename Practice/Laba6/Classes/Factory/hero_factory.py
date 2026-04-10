from typing import Union

from ..Character.mage import Mage
from ..Character.warrior import Warrior
from ..weapon import Weapon


class HeroFactory:
    @staticmethod
    def create_hero(hero_type: str, name: str, weapon: Weapon) -> Union[Warrior, Mage]:
        hero_map = {"warrior": Warrior, "mage": Mage}
        if hero_type.lower() not in hero_map:
            raise ValueError("Неизвестный тип героя. Доступны: 'warrior', 'mage'")
        return hero_map[hero_type.lower()](name, weapon)

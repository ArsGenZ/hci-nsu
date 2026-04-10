from abc import ABC, abstractmethod

from ..decorators import log_action
from ..weapon import Weapon


class Hero(ABC):
    """Абстрактный базовый класс героя."""

    def __init__(self, name: str, base_power: int, base_health: int, weapon: Weapon):
        self.name = name
        self._base_power = base_power
        self._base_health = base_health
        self.level = 1
        self.experience = 0
        self.weapon = weapon
        self.is_alive = True

    @property
    def power(self) -> int:
        return self._base_power + (self.level * 5) + self.weapon.power_bonus

    @property
    def health(self) -> int:
        return self._base_health + (self.level * 20)

    @abstractmethod
    def scout(self) -> str:
        pass

    @log_action
    def fight(self, enemy) -> bool:
        print(f"{self.name} вступает в бой с {enemy.name}!")
        return True

    def gain_experience(self, amount: int):
        if not self.is_alive:
            return
        self.experience += amount
        if self.experience < 0:
            self.experience = 0
        self._check_level_up()

    def _check_level_up(self):
        threshold = self.level * 100
        if self.experience >= threshold:
            self.level_up()
            self.experience = 0

    @abstractmethod
    def level_up(self):
        pass

    def __str__(self):
        status = "Мертв" if not self.is_alive else f"HP: {self.health}"
        return f"[{self.name}] (Ур. {self.level}) | {status} | Сила: {self.power} | Опыт: {self.experience}/{self.level * 100}"

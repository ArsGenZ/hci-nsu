from ..decorators import log_action
from ..weapon import Weapon
from .hero import Hero


class Warrior(Hero):
    def __init__(self, name: str, weapon: Weapon):
        super().__init__(name, base_power=45, base_health=120, weapon=weapon)

    @log_action
    def scout(self) -> str:
        return f"{self.name} идет в разведку, проверяя тропы и лагеря врагов."

    def level_up(self):
        self.level += 1
        self._base_power += 8
        self._base_health += 30
        print(
            f"Воин {self.name} достиг уровня {self.level}! +8 к силе, +30 к здоровью."
        )

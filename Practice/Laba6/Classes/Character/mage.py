from ..decorators import log_action
from ..weapon import Weapon
from .hero import Hero


class Mage(Hero):
    def __init__(self, name: str, weapon: Weapon):
        super().__init__(name, base_power=35, base_health=90, weapon=weapon)

    @log_action
    def scout(self) -> str:
        return f"{self.name} сканирует местность магическим зрением, выявляя угрозы и тайники."

    def level_up(self):
        self.level += 1
        self._base_power += 12
        self._base_health += 20
        print(
            f"Маг {self.name} достиг уровня {self.level}! +12 к силе, +20 к здоровью."
        )

import random

from ..enemy import Enemy


class EnemyFactory:
    @staticmethod
    def create_random_enemy() -> Enemy:
        names = ["Гоблин", "Орк", "Тролль", "Бандит", "Древний Волк"]
        name = random.choice(names)
        power = random.randint(30, 70)
        health = random.randint(50, 110)
        return Enemy(name, power, health)

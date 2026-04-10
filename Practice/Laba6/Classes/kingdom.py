class Kingdom:
    """Инкапсуляция ресурсов королевства."""

    def __init__(self, name: str, territory: int = 100, food: int = 100):
        self._name = name
        self._territory = territory
        self._food = food

    @property
    def territory(self) -> int:
        return self._territory

    @territory.setter
    def territory(self, value: int):
        self._territory = max(0, value)

    @property
    def food(self) -> int:
        return self._food

    @food.setter
    def food(self, value: int):
        self._food = max(0, value)

    def gain_resources(self, territory: int, food: int):
        self.territory += territory
        self.food += food
        print(f"Королевство получило: +{territory} территории, +{food} продовольствия.")

    def lose_resources(self, territory: int, food: int):
        self.territory -= territory
        self.food -= food
        print(f"Королевство потеряло: -{territory} территории, -{food} продовольствия.")

    def is_alive(self) -> bool:
        return self._territory > 0 and self._food > 0

    def battle_probability(self, hero, enemy) -> float:
        """Рассчитывает вероятность победы героя в бою с врагом"""
        hero_power = hero.power + hero.level
        enemy_power = enemy.get_power()
        if hero_power + enemy_power == 0:
            return 50.0
        probability = (hero_power / (hero_power + enemy_power)) * 100
        return round(probability, 2)

    def __str__(self):
        return f"[Королевство '{self._name}'] Территория: {self._territory} | Продовольствие: {self._food}"

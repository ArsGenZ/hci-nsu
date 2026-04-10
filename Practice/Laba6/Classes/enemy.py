class Enemy:
    def __init__(self, name: str, power: int, health: int):
        self.name = name
        self._power = power
        self._health = health

    def get_power(self) -> int:
        return self._power

    def get_health(self) -> int:
        return self._health

    def __str__(self):
        return f"[{self.name}] | Сила: {self._power} | Здоровье: {self._health}"

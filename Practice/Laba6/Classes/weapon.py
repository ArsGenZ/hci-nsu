class Weapon:
    """Класс оружия (Композиция)."""

    def __init__(self, name: str, power_bonus: int):
        self.name = name
        self.power_bonus = power_bonus

    def __str__(self):
        return f"{self.name} (+{self.power_bonus} к силе)"

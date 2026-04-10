from .combat_strategy import CombatStrategy


class AggressiveStrategy(CombatStrategy):
    def modify_probability(self, base_prob: float) -> float:
        return round(min(base_prob * 1.15, 99.0), 2)

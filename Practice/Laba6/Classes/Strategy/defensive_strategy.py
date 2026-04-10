from .combat_strategy import CombatStrategy


class DefensiveStrategy(CombatStrategy):
    def modify_probability(self, base_prob: float) -> float:
        return round(max(base_prob * 0.85, 15.0), 2)

from .combat_strategy import CombatStrategy


class BalancedStrategy(CombatStrategy):
    def modify_probability(self, base_prob: float) -> float:
        return base_prob

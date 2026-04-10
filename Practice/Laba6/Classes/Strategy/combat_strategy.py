from abc import ABC, abstractmethod


class CombatStrategy(ABC):
    @abstractmethod
    def modify_probability(self, base_prob: float) -> float:
        pass

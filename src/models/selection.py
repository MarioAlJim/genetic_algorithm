"""This file is for defining the selection class and its child classes"""
import random

class Selection:
    """Selection class"""
    def __init__(self) -> None:
        self._rate = 0.5

    @property
    def rate(self):
        """Get selection rate"""
        return self._rate

    @rate.setter
    def rate(self, rate: float) -> None:
        """Set selection rate"""
        if 0 <= rate <= 1:
            self._rate = rate
        else:
            raise ValueError('Selection rate must be between 0 and 1')

class RandomSelection(Selection):
    """Random selection class"""
    def select(self, pop: list, pop_size: int) -> None:
        """Randomly selects parents"""
        random.sample(pop, int(self._rate * pop_size))

class SteadyState(Selection):
    """Steady state selection class"""
    def select(self, pop: list, pop_size: int) -> list:
        """Sorts population by fitness score and then selects the new population"""
        sorted_pop = sorted(pop, key=lambda x: x[1])
        selected_pop = sorted_pop[:int(self._rate * pop_size)]
        return selected_pop

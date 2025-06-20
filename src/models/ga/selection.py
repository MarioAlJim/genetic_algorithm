"""This file is for defining the selection class and its child classes"""
from random import sample

class Selection:
    """Selection class"""
    def __init__(self, rate: float) -> None:
        self._type = 'Selection'
        self._rate = rate

    @property
    def type(self) -> str:
        """Get selection type"""
        return self._type

    @property
    def rate(self) -> float:
        """Get selection rate"""
        return self._rate

    @rate.setter
    def rate(self, rate: float) -> None:
        """Set selection rate"""
        if 0.1 <= rate <= 1:
            self._rate = rate
        else:
            raise ValueError('Selection rate must be between 0.1 and 1')

    def select(self, pop: list, sel_size: int) -> list:
        """Selection method"""
        raise NotImplementedError('Selection method should be implemented by child class')

class RandomSelection(Selection):
    """Random selection class

    Randomly selects population
    """
    def __init__(self, rate: float) -> None:
        super().__init__(rate)
        self._type = "Random"

    def select(self, pop: list, sel_size: int) -> list:
        return sample(pop, sel_size)

class SteadyState(Selection):
    """Steady state selection class

    Sorts population by fitness score and then selects the new population
    """
    def __init__(self, rate: float) -> None:
        super().__init__(rate)
        self._type = "Steady state"

    def select(self, pop: list, sel_size: int) -> list:
        sorted_pop = sorted(pop, key=lambda x: x[1], reverse=True)
        return sorted_pop[:sel_size]

"""This file is for defining the crossover classes"""
from random import randint, shuffle

class Crossover:
    """Crossover class"""
    def __init__(self) -> None:
        self._type = 'Crossover'

    @property
    def type(self) -> str:
        """Get crossover type"""
        return self._type

    def cross(self, chromo_len: int, parent1: list, parent2: list) -> list:
        """Crossover method"""
        raise NotImplementedError('Crossover method should be implemented by child class')

class OnePoint(Crossover):
    """One point crossover class

    Exchanges the chromosome genes as from one point
    """
    def __init__(self) -> None:
        super().__init__()
        self._type = "One point"

    def cross(self, chromo_len: int, parent1: list, parent2: list) -> list:
        # Creates children
        point = randint(1, chromo_len - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return [child1, child2]

class TwoPoint(Crossover):
    """Two point crossover class

    Exchanges the chromosome genes as from two points
    """
    def __init__(self) -> None:
        super().__init__()
        self._type = "Two point"

    def cross(self, chromo_len: int, parent1: list, parent2: list) -> list:
        point1 = randint(1, (chromo_len - 2))
        point2 = randint(point1 + 1, (chromo_len - 1))
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

        return [child1, child2]

class Uniform(Crossover):
    """Uniform crossover class

    Exchanges the chromosome genes uniformly
    """
    def __init__(self) -> None:
        super().__init__()
        self._type = "Uniform"

    def cross(self, chromo_len: int, parent1: list, parent2: list) -> list:
        parents = [parent1, parent2]

        child1 = []
        child2 = []
        for gen in range(chromo_len):
            shuffle(parents)
            child1.append(parents[0][gen])
            child2.append(parents[1][gen])

        return [child1, child2]

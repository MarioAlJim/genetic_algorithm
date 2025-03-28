"""This file is for defining the crossover classes"""
import random

class Crossover:
    """Crossover class"""
    def __init__(self) -> None:
        self._type = 'Crossover'

    @property
    def type(self) -> str:
        """Get crossover type"""
        return self._type

    def cross(self, chromo_len: int, parent1, parent2) -> list:
        """Crossover method"""
        raise NotImplementedError('Crossover method should be implemented by child class')

class OnePointCrossover(Crossover):
    """One point crossover class

    Exchanges the chromosome genes as from one point
    """
    def __init__(self) -> None:
        self._type = 'one-point'

    def cross(self, chromo_len: int, parent1, parent2) -> list:
        # Creates children
        point = random.randint(1, chromo_len - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return [child1, child2]

class TwoPointCrossover(Crossover):
    """Two point crossover class

    Exchanges the chromosome genes as from two points
    """
    def __init__(self) -> None:
        self._type = 'two-point'

    def cross(self, chromo_len: int, parent1, parent2) -> list:
        point1 = random.randint(1, (chromo_len - 2))
        point2 = random.randint(point1 + 1, (chromo_len - 1))
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

        return [child1, child2]

class UniformCrossover(Crossover):
    """Uniform crossover class

    Exchanges the chromosome genes uniformly
    """
    def __init__(self) -> None:
        self._type = 'uniform'

    def cross(self, chromo_len: int, parent1, parent2) -> list:
        parents = [parent1, parent2]

        child1 = []
        child2 = []
        for chromo in range(chromo_len):
            random.shuffle(parents)
            child1.append(parents[0][chromo])
            child2.append(parents[1][chromo])

        return [child1, child2]

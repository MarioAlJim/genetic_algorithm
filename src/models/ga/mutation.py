"""This file is for defining the mutation class and its child classes"""
from random import random

class Mutation:
    """Mutation class"""
    def __init__(self, rate: float):
        self._type = 'Mutation'
        self._rate = rate

    @property
    def type(self) -> str:
        """Get mutation type"""
        return self._type

    @property
    def rate(self) -> float:
        """Get mutation rate"""
        return self._rate

    @rate.setter
    def rate(self, rate: float) -> None:
        """Set mutation rate"""
        if 0 <= rate <= 1:
            self._rate = rate
        else:
            raise ValueError('Mutation rate must be between 0 and 1')

    def mutate(self, offspring: list, chromo_len: int, create_gen) -> list:
        """Mutation method"""
        raise NotImplementedError('Mutation method should be implemented by child class')

class RandomResetting(Mutation):
    """Random resetting class

    Mutates the offspring randomly
    """
    def __init__(self, rate: float):
        super().__init__(rate)
        self._type = "Random resetting"

    def mutate(self, offspring: list, chromo_len: int, create_gen) -> list:
        mutated_offspring = []
        for child in offspring:
            for i in range(chromo_len):
                if self._rate > random():
                    child[i] = create_gen()
            mutated_offspring.append(child)

        return mutated_offspring

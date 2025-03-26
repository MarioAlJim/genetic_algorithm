'''This class is for defining the selection class and its child classes'''
import random

class Selection:
    '''Selection parent class'''
    def __init__(self) -> None:
        self._rate = 0.5

    @property
    def rate(self):
        """Get selection rate"""
        return self._rate

    @rate.setter
    def rate(self, rate: float) -> None:
        '''Selection rate setter'''
        if 0 <= rate <= 1:
            self._rate = rate
        else:
            raise ValueError('Selection rate must be between 0 and 1')

class RandomSelection(Selection):
    '''Random selection class'''
    def select(self, pop: list, pop_size: int) -> None:
        '''Randomly selects (__rate)% parents'''
        random.sample(pop, int(self._rate * pop_size))

class SteadyState(Selection):
    '''Steady state selection class'''
    def select(self, pop: list, pop_size: int) -> list:
        '''Sorts population by fitness score and then selects the (__rate)%'''
        sorted_pop = sorted(pop, key=lambda x: x[1])
        selected_pop = sorted_pop[:int(self._rate * pop_size)]
        return selected_pop

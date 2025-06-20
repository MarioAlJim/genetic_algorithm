"""File for gen class and its children"""
from random import uniform

class Gen:
    """Gen class"""
    def __init__(self) -> None:
        self._type = 'Gen'

    @property
    def type(self) -> str:
        """Get gen type"""
        return self._type

    def create(self):
        """Create gen method"""
        raise NotImplementedError('Create method should be implemented by child class')

class RealNumber(Gen):
    """Real number class"""
    def __init__(self):
        super().__init__()
        self._type = "Real number"
        self._min_value = -100
        self._max_value = 100

    @property
    def min_value(self) -> float:
        """Get min value"""
        return self._min_value

    @min_value.setter
    def min_value(self, value: float) -> None:
        """Set min value"""
        if value < self._max_value:
            self._min_value = value
        else:
            raise ValueError('Min value must be less than max value')

    @property
    def max_value(self) -> float:
        """Get max value"""
        return self._max_value

    @max_value.setter
    def max_value(self, value: float) -> None:
        """Set max value"""
        if value > self._min_value:
            self._max_value = value
        else:
            raise ValueError('Max value must be greater than min value')

    def create(self) -> float:
        """Create real number gen"""
        return round(uniform(self.min_value, self.max_value), 2)

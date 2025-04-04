"""This file is for defining the genetic algorithm"""
from src.models.fitness_evaluation import score_triangle_classification
from src.models.mutation import RandomResetting
from src.models.selection import *
from src.models.crossover import *

class GeneticAlgorithm:
    """Class for the configuration and execution of the genetic algorithm

    Configurable attributes:
    - chromo_len
    - pop_size
    - num_generations
    - expected_solution
    - selection (type and rate)
    - crossover (type)
    - mutation (type and rate)
    - current_pop
    """
    def __init__(self) -> None:
        self._chromo_len = 3
        self._pop_size = 10
        self._num_generations = 50
        self._fitness_function = score_triangle_classification
        self._expected_solution = 'scalene'
        self._selection = RandomSelection(0.5)
        self._crossover = UniformCrossover()
        self._mutation = RandomResetting(0.3)
        self._current_pop = []

    @property
    def chromo_len(self) -> int:
        """Get chromosome length"""
        return self._chromo_len

    @chromo_len.setter
    def chromo_len(self, chromo_len: int):
        """Set chromosome length"""
        min_len = 1
        max_len = 9999

        if min_len <= chromo_len <= max_len:
            self._chromo_len = chromo_len
        else:
            raise ValueError(
                'Chromosome length must be between',
                min_len,'and',max_len
            )

    @property
    def pop_size(self) -> int:
        """Get population size"""
        return self._pop_size

    @pop_size.setter
    def pop_size(self, pop_size: int):
        """Set population size"""
        min_pop = 1
        max_pop = 9999

        if min_pop <= pop_size <= max_pop:
            self._pop_size = pop_size
        else:
            raise ValueError(
                'Population must be between',
                min_pop,'and',max_pop
            )

    @property
    def num_generations(self) -> int:
        """Get number of generations"""
        return self._num_generations

    @num_generations.setter
    def num_generations(self, num_generations: int):
        """Set number of generations"""
        min_generations = 1
        max_generations = 9999

        if min_generations <= num_generations <= max_generations:
            self._num_generations = num_generations
        else:
            raise ValueError(
                'Number of generations must be between',
                min_generations,'and',max_generations
            )

    @property
    def expected_solution(self) -> str:
        """Get expected solution"""
        return self._expected_solution

    @expected_solution.setter
    def expected_solution(self, expected_solution):
        """Set expected solution"""
        expected_solutions = []

        if self._fitness_function == score_triangle_classification:
            expected_solutions = ['scalene', 'equilateral', 'isosceles', 'invalid', 'out of range']

        if expected_solution not in expected_solutions:
            raise ValueError('Expected solution must be in', expected_solutions)

        self._expected_solution = expected_solution

    @property
    def selection_rate(self) -> float:
        """Get selection rate"""
        return self._selection.rate

    @selection_rate.setter
    def selection_rate(self, selection_rate: float):
        """Set selection rate"""
        if 0 <= selection_rate <= 1:
            self._selection.rate = selection_rate
        else:
            raise ValueError('Selection rate must be between 0 and 1')

    @property
    def selection_type(self) -> str:
        """Get selection type"""
        return self._selection.type

    @selection_type.setter
    def selection_type(self, selection_type: str):
        """Set selection type"""
        selection_types = ['random', 'steady-state']
        selection_classes = [RandomSelection, SteadyState]

        if selection_type not in selection_types:
            raise ValueError('Selection type must be a valid value')

        rate = self._selection.rate

        for i, sel_type in enumerate(selection_types):
            if selection_type == sel_type:
                self._selection = selection_classes[i](rate)
                break

    @property
    def crossover_type(self) -> str:
        """Get crossover type"""
        return self._crossover.type

    @crossover_type.setter
    def crossover_type(self, crossover_type: str):
        """Set crossover type"""
        crossover_types = ['one-point', 'two-point', 'uniform']
        crossover_classes = [OnePointCrossover, TwoPointCrossover, UniformCrossover]

        if crossover_type not in crossover_types:
            raise ValueError('Crossover type must be a valid value')

        for i, cross_type in enumerate(crossover_types):
            if crossover_type == cross_type:
                self._crossover = crossover_classes[i]()
                break

    @property
    def mutation_rate(self) -> float:
        """Get mutation rate"""
        return self._mutation.rate

    @mutation_rate.setter
    def mutation_rate(self, mutation_rate: float):
        """Set mutation rate"""
        if 0 <= mutation_rate <= 1:
            self._mutation.rate = mutation_rate
        else:
            raise ValueError('Mutation rate must be between 0 and 1')

    @property
    def mutation_type(self) -> str:
        """Get mutation type"""
        return self._mutation.type

    @mutation_type.setter
    def mutation_type(self, mutation_type: str):
        """Set mutation type"""
        mutation_types = ['random-resetting']
        mutation_classes = [RandomResetting]

        if mutation_type not in mutation_types:
            raise ValueError('Mutation type must be a valid value')

        rate = self._mutation.rate

        for i, mut_type in enumerate(mutation_types):
            if mutation_type == mut_type:
                self._mutation = mutation_classes[i](rate)
                break

    @property
    def current_pop(self) -> list:
        """Get current population"""
        return self._current_pop

    @current_pop.setter
    def current_pop(self, current_pop: list):
        """Set current population"""
        if current_pop:
            self._current_pop = current_pop
        else:
            raise ValueError('Current population must have individuals')

    def create_gen(self) -> int:
        """Creates a gen according to gen type"""
        gen = random.randint(0,100)
        return gen

    def init_pop(self) -> list:
        """Initializes the population"""
        population = []

        for _ in range(self._pop_size):
            chromosome = []
            for _ in range(self._chromo_len):
                chromosome.append(self.create_gen())
            population.append(chromosome)

        return population

    def evaluate_pop(self, pop: list) -> list:
        """Evaluates the population"""
        evaluated_pop = []

        for chromo in pop:
            evaluated_chromo = self._fitness_function(chromo, self._expected_solution)
            evaluated_pop.append(evaluated_chromo)

        return evaluated_pop

    def selection(self, new_pop: list) -> list:
        """Selects a percentage of the new population for the next generation"""
        return self._selection.select(new_pop, self._pop_size)

    def crossover(self, current_pop: list, new_pop: list) -> list:
        """Selects random parents according to the selected crossover"""
        offspring = []

        for _ in range(self._pop_size):
            # Gets the chromosome parents from the evaluated lists
            parent1 = random.choice(new_pop)[0]
            parent2 = random.choice(current_pop)[0]

            children = self._crossover.cross(self._chromo_len, parent1, parent2)
            offspring.extend([random.choice(children)])

        return offspring

    def mutate(self, offspring: list) -> list:
        """Mutates the offspring population"""
        return self._mutation.mutate(offspring, self._chromo_len, self.create_gen)

    def replace(self, new_pop, current_pop):
        """Replaces chromosomes if new gen chromosomes have better fitness score"""
        for _ in range(self._pop_size):
            if current_pop[_][1] > new_pop[_][1]:
                # Replaces chromosome
                current_pop[_][0] = new_pop[_][0]
                # Replaces fitness score
                current_pop[_][1] = new_pop[_][1]

        return current_pop

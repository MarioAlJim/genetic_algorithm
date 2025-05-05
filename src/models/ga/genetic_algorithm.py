"""This file is for defining the genetic algorithm"""
from random import choice

from src.models.algorithm import Algorithm
from src.models.ga.crossover import OnePoint, TwoPoint, Uniform
from src.models.ga.gen import RealNumber
from src.models.ga.mutation import RandomResetting
from src.models.ga.selection import RandomSelection, SteadyState

class GeneticAlgorithm(Algorithm):
    """Class for the configuration and execution of the genetic algorithm

    Configurable attributes:
    - gen type
    - chromo length
    - population size
    - number of generations
    - selection type and rate
    - crossover type
    - mutation type and rate
    - current population
    - evaluation (fitness function)
    - expected solution
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = 'genetic-algorithm'
        self._gens = [
            ['real-number', RealNumber],
        ]
        self._selections = [
            ['random', RandomSelection],
            ['steady-state', SteadyState],
        ]
        self._crossovers = [
            ['one-point', OnePoint],
            ['two-point', TwoPoint],
            ['uniform', Uniform],
        ]
        self._mutations = [
            ['random-resetting', RandomResetting],
        ]
        self._gen = RealNumber()
        self._chromo_len = 3
        self._pop_size = 10
        self._num_generations = 50
        self._selection = RandomSelection(0.5)
        self._crossover = Uniform()
        self._mutation = RandomResetting(0.3)
        self._current_pop = []

    @property
    def gen_type(self) -> str:
        """Get gen type"""
        return self._gen.type

    @gen_type.setter
    def gen_type(self, gen_type: str):
        """Set gen type"""
        for name, gen in self._gens:
            if gen_type == name:
                self._gen = gen()
                return

        raise ValueError('Gen type must be a valid value: ', self._gens)

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
        max_pop = 10

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
        max_generations = 10

        if min_generations <= num_generations <= max_generations:
            self._num_generations = num_generations
        else:
            raise ValueError(
                'Number of generations must be between',
                min_generations,'and',max_generations
            )

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
        for name, selection in self._selections:
            if selection_type == name:
                self._selection = selection(self._selection.rate)
                return

        raise ValueError('Selection type must be a valid value: ', self._selections)

    @property
    def crossover_type(self) -> str:
        """Get crossover type"""
        return self._crossover.type

    @crossover_type.setter
    def crossover_type(self, crossover_type: str):
        """Set crossover type"""
        for name, crossover in self._crossovers:
            if crossover_type == name:
                self._crossover = crossover()
                return

        raise ValueError('Crossover type must be a valid value: ', self._crossovers)

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
        for name, mutation in self._mutations:
            if mutation_type == name:
                self._mutation = mutation(self._mutation.rate)
                return
        raise ValueError('Mutation type must be a valid value: ', self._mutations)

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

    def create_gen(self):
        """Creates a gen according to gen type"""
        return self._gen.create()

    def init_pop(self) -> list:
        """Initializes the population"""
        population = []

        for _ in range(self.pop_size):
            chromosome = []
            for _ in range(self.chromo_len):
                chromosome.append(self.create_gen())
            population.append(chromosome)

        evaluated_pop = self.evaluate(population)
        self.current_pop = evaluated_pop
        return evaluated_pop

    def evaluate(self, pop: list) -> list:
        """Evaluates the population"""
        evaluated_pop = []

        for chromo in pop:
            evaluated_chromo = self._evaluation.score(chromo, self.expected_solution)
            evaluated_pop.append(evaluated_chromo)

        return evaluated_pop

    def select(self, new_pop: list) -> list:
        """Selects a percentage of the new population for the next generation"""
        return self._selection.select(new_pop, self.pop_size)

    def cross(self, sel_pop: list) -> list:
        """Selects random parents according to the selected crossover"""
        offspring = []

        for _ in range(self.pop_size):
            # Gets the chromosome parents from the selected population
            parent1 = choice(sel_pop)[0]
            parent2 = choice(sel_pop)[0]

            children = self._crossover.cross(self.chromo_len, parent1, parent2)
            offspring.extend([choice(children)])

        return offspring

    def mutate(self, offspring: list) -> list:
        """Mutates the offspring population"""
        return self._mutation.mutate(offspring, self.chromo_len, self.create_gen)

    def execute(self) -> tuple:
        """Executes the genetic algorithm"""
        self.init_pop()
        current_generation = 1
        generations = []
        initial_pops = []
        selected_pops = []
        crossover_pops = []
        mutated_pops = []
        evaluated_pops = []

        while current_generation <= self.num_generations:
            selected_pop = self.select(self.current_pop)
            offspring = self.cross(selected_pop)
            mutated_offspring = self.mutate(offspring)
            new_pop = self.evaluate(mutated_offspring)

            generations.append(current_generation)
            initial_pops.append(self.current_pop)
            selected_pops.append(selected_pop)
            crossover_pops.append(offspring)
            mutated_pops.append(mutated_offspring)
            evaluated_pops.append(new_pop)

            self.current_pop = new_pop
            current_generation += 1

        config = {
            "Evaluation type": [self.evaluation],
            "Expected solution": [self.expected_solution],
            "Algorithm": [self.name],
            "Generations": [self.num_generations],
            "Population size": [self.pop_size],
            "Chromosome length": [self.chromo_len],
            "Gen type": [self.gen_type],
            "Selection type": [self.selection_type],
            "Selection rate": [self.selection_rate],
            "Crossover type": [self.crossover_type],
            "Mutation type": [self.mutation_type],
            "Mutation rate": [self.mutation_rate],
        }
        exec_data = {
            "Generation": generations,
            "Initial population": initial_pops,
            "Selected population": selected_pops,
            "Crossover population": crossover_pops,
            "Mutated population": mutated_pops,
            "Evaluated population": evaluated_pops,
        }

        return config, exec_data

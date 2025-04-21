"""This file is for defining the genetic algorithm"""
from random import choice
from src.models.crossover import OnePoint, TwoPoint, Uniform
from src.models.evaluation import TriangleClassification
from src.models.gen import RealNumber
from src.models.mutation import RandomResetting
from src.models.selection import RandomSelection, SteadyState
from time import sleep

class GeneticAlgorithm:
    """Class for the configuration and execution of the genetic algorithm

    Configurable attributes:
    - gen_type
    - chromo_len
    - pop_size
    - num_generations
    - fitness_function
    - expected_solution
    - selection (type and rate)
    - crossover (type)
    - mutation (type and rate)
    - current_pop
    """
    def __init__(self) -> None:
        self._gen = RealNumber()
        self._chromo_len = 3
        self._pop_size = 10
        self._num_generations = 50
        self._fitness_function = TriangleClassification()
        self._expected_solution = 'scalene'
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
        gens = [
            ['real-number', RealNumber],
        ]

        for name, gen in gens:
            if gen_type == name:
                self._gen = gen()
                return

        raise ValueError('Gen type must be a valid value')

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
    def fitness_function(self) -> str:
        return self._fitness_function.name

    @fitness_function.setter
    def fitness_function(self, fitness_function: str):
        """Set fitness function"""
        fitness_functions = [
            ['triangle-classification', TriangleClassification],
        ]

        for name, evaluation in fitness_functions:
            if fitness_function == name:
                self._fitness_function = evaluation()
                return

        raise ValueError('Fitness function must be a valid value')

    @property
    def expected_solution(self) -> str:
        """Get expected solution"""
        return self._expected_solution

    @expected_solution.setter
    def expected_solution(self, expected_solution):
        """Set expected solution"""
        expected_solutions = self._fitness_function.expected_solutions

        if expected_solution not in expected_solutions:
            raise ValueError('Expected solution must be: ', expected_solutions)

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
        selections = [
            ['random', RandomSelection],
            ['steady-state', SteadyState],
        ]

        for name, selection in selections:
            if selection_type == name:
                self._selection = selection(self._selection.rate)
                return

        raise ValueError('Selection type must be a valid value')

    @property
    def crossover_type(self) -> str:
        """Get crossover type"""
        return self._crossover.type

    @crossover_type.setter
    def crossover_type(self, crossover_type: str):
        """Set crossover type"""
        crossovers = [
            ['one-point', OnePoint],
            ['two-point', TwoPoint],
            ['uniform', Uniform],
        ]

        for name, crossover in crossovers:
            if crossover_type == name:
                self._crossover = crossover()
                return

        raise ValueError('Crossover type must be a valid value')

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
        mutations = [
            ['random-resetting', RandomResetting],
        ]

        for name, mutation in mutations:
            if mutation_type == name:
                self._mutation = mutation(self._mutation.rate)
                return
        raise ValueError('Mutation type must be a valid value')

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
            evaluated_chromo = self._fitness_function.score(chromo, self.expected_solution)
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

    def execute(self, exec_data: dict, conf: dict) -> None:
        """Executes the genetic algorithm"""
        conf = {
            "Configuration": {
                "generations": self.num_generations,
                "population": {
                    "size": self.pop_size,
                    "chromosomes": {
                        "length": self.chromo_len,
                        "gen_type": self.gen_type,
                    },
                },
                "evaluation": {
                    "type": self.fitness_function,
                    "expected_solution": self.expected_solution,
                },
                "selection": {
                    "type": self.selection_type,
                    "rate": self.selection_rate,
                },
                "crossover": {
                    "type": self.crossover_type,
                },
                "mutation": {
                    "type": self.mutation_type,
                    "rate": self.mutation_rate,
                }
            }
        }

        self.init_pop()
        current_generation = 1

        while current_generation <= self.num_generations:
            selected_pop = self.select(self.current_pop)
            offspring = self.cross(selected_pop)
            mutated_offspring = self.mutate(offspring)
            new_pop = self.evaluate(mutated_offspring)

            generation = {
                "generation_" + str(current_generation): {
                    "initial_population": self.current_pop,
                    "selected": selected_pop,
                    "crossovered": offspring,
                    "mutated": mutated_offspring,
                    "evaluated": new_pop,
                }
            }
            exec_data.update(generation)

            sleep(0.5)
            self.current_pop = new_pop
            current_generation += 1

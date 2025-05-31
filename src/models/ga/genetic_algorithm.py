"""This file is for defining the genetic algorithm"""
from random import choice
from flask_babel import gettext
from src.models.algorithm import Algorithm
from src.models.ga.crossover import OnePoint, TwoPoint, Uniform
from src.models.ga.gen import RealNumber
from src.models.ga.mutation import RandomResetting
from src.models.ga.selection import RandomSelection, SteadyState

class GeneticAlgorithm(Algorithm):
    """Class for the configuration and execution of the genetic algorithm

    Configurable attributes:
    - population size
    - number of generations
    - selection type and rate
    - crossover type
    - mutation type and rate
    - evaluation (fitness function)
    - elitism rate

    Other attributes:
    - gen type
    - chromosome length
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = gettext("Genetic Algorithm")
        self._gen = RealNumber()
        self._chromo_len = self._evaluation.inputs * self._evaluation.branches
        self._pop_size = 10
        self._num_generations = 10
        self._selection = RandomSelection(0.5)
        self._crossover = Uniform()
        self._mutation = RandomResetting(0.5)
        self._elite_pop_rate = 0.1

        self._current_pop = []
        self._elite_pop = []

    @property
    def evaluation(self) -> str:
        """Get evaluation"""
        return self._evaluation.name

    @evaluation.setter
    def evaluation(self, evaluation) -> None:
        """Set evaluation

        Based on the evaluation, it sets also the gen type and chromosome length
        """
        for name, eval_class in self._evaluations:
            if name == evaluation:
                self._evaluation = eval_class()
                self._set_gen_type(self._evaluation.input_type)
                self._chromo_len = self._evaluation.inputs * self._evaluation.branches
                return

        raise ValueError('Evaluation must be a valid value: ', self._evaluations)

    def _set_gen_type(self, gen_type: str) -> None:
        """Set gen type"""
        gens = [
            ['real-number', RealNumber],
        ]

        for name, gen in gens:
            if gen_type == name:
                self._gen = gen()
                return

        raise ValueError('Gen type must be a valid value: ', gens)

    @property
    def gen_type(self) -> str:
        """Get gen type"""
        return self._gen.type

    @property
    def chromo_len(self) -> int:
        """Get chromosome length"""
        return self._chromo_len

    @property
    def pop_size(self) -> int:
        """Get population size"""
        return self._pop_size

    @pop_size.setter
    def pop_size(self, pop_size: int):
        """Set population size"""
        min_pop = 1
        max_pop = 50

        if (isinstance(pop_size, int) and
                min_pop <= pop_size <= max_pop):
            self._pop_size = pop_size
        else:
            raise ValueError(
                'Population must be an int between',
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
        max_generations = 100

        if (isinstance(num_generations, int) and
                min_generations <= num_generations <= max_generations):
            self._num_generations = num_generations
        else:
            raise ValueError(
                'Number of generations must be an int between',
                min_generations,'and',max_generations
            )

    @property
    def selection_rate(self) -> float:
        """Get selection rate"""
        return self._selection.rate

    @selection_rate.setter
    def selection_rate(self, selection_rate: float):
        """Set selection rate"""

        if (isinstance(selection_rate, float) and
                0 <= selection_rate <= 1):
            self._selection.rate = selection_rate
        else:
            raise ValueError('Selection rate must be a float between 0.0 and 1.0')

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

        raise ValueError('Selection type must be a valid value: ', selections)

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

        raise ValueError('Crossover type must be a valid value: ', crossovers)

    @property
    def mutation_rate(self) -> float:
        """Get mutation rate"""
        return self._mutation.rate

    @mutation_rate.setter
    def mutation_rate(self, mutation_rate: float):
        """Set mutation rate"""
        if (isinstance(mutation_rate, float) and
                0 <= mutation_rate <= 1):
            self._mutation.rate = mutation_rate
        else:
            raise ValueError('Mutation rate must be a float between 0.0 and 1.0')

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
        raise ValueError('Mutation type must be a valid value: ', mutations)

    @property
    def elite_pop_rate(self) -> float:
        """Get percentage of elite population"""
        return self._elite_pop_rate

    @elite_pop_rate.setter
    def elite_pop_rate(self, elite_pop_rate: float):
        """Set percentage of elite population"""
        if (isinstance(elite_pop_rate, float) and
                0 <= elite_pop_rate <= 1):
            self._elite_pop_rate = elite_pop_rate
        else:
            raise ValueError('Elitism rate must be a float between 0.0 and 1.0')

    def _create_gen(self):
        """Creates a gen according to gen type"""
        return self._gen.create()

    def _init_pop(self) -> list:
        """Initializes the population"""
        population = []

        for _ in range(self.pop_size):
            chromosome = []
            for _ in range(self.chromo_len):
                chromosome.append(self._create_gen())
            population.append(chromosome)

        evaluated_pop = self._evaluate(population)
        self._current_pop = evaluated_pop
        return evaluated_pop

    def _evaluate(self, pop: list) -> list:
        """Evaluates the population"""
        evaluated_pop = []

        for chromo in pop:
            evaluated_chromo = self._evaluation.score(chromo)
            evaluated_pop.append(evaluated_chromo)

        return evaluated_pop

    def _init_elite(self) -> list:
        """Gets the elite population"""
        sorted_pop = sorted(self._current_pop, key=lambda x: x[1], reverse=True)
        evaluated_elite = sorted_pop[:int(self.elite_pop_rate * self.pop_size)]
        elite = [evaluated_chromo[0] for evaluated_chromo in evaluated_elite]
        self._elite_pop = elite
        return elite

    def _select(self, new_pop: list) -> list:
        """Selects a percentage of the new population for the next generation"""
        sel_size = int(self.selection_rate * self.pop_size)
        full_sample =  self._selection.select(new_pop, 1 if sel_size == 0 else sel_size)
        return [evaluated_chromo[0] for evaluated_chromo in full_sample]

    def _cross(self, sel_pop: list) -> list:
        """Selects random parents according to the selected crossover"""
        offspring = []

        for _ in range(self.pop_size - len(self._elite_pop)):
            # Gets the chromosome parents from the selected population
            parent1 = choice(sel_pop)
            parent2 = choice(sel_pop)

            children = self._crossover.cross(self.chromo_len, parent1, parent2)
            offspring.extend([choice(children)])

        return offspring

    def _mutate(self, offspring: list) -> list:
        """Mutates the offspring population"""
        mutated_offspring = self._mutation.mutate(offspring, self.chromo_len, self._create_gen)
        return mutated_offspring

    def execute(self) -> tuple:
        """Executes the genetic algorithm.

        Returns a tuple: config, exec_data
        """
        self._init_pop()
        generations = []
        initial_pops = []
        selected_pops = []
        crossover_pops = []
        mutated_pops = []
        evaluated_pops = []

        for current_generation in range(self.num_generations):
            self._init_elite()
            selected_pop = self._select(self._current_pop)
            offspring = self._cross(selected_pop)
            mutated_offspring = self._mutate(offspring)
            new_pop = self._evaluate(self._elite_pop + mutated_offspring)

            generations.append(current_generation+1)
            initial_pops.append(sorted(self._current_pop, key=lambda x: x[1], reverse=True))
            selected_pops.append(selected_pop)
            crossover_pops.append(offspring)
            mutated_pops.append(mutated_offspring)
            evaluated_pops.append(sorted(new_pop, key=lambda x: x[1], reverse=True))

            self._current_pop = new_pop

        config = {
            gettext("Evaluation type"): [self.evaluation],
            gettext("Algorithm"): [self.name],
            gettext("Generations"): [self.num_generations],
            gettext("Population size"): [self.pop_size],
            gettext("Chromosome length"): [self.chromo_len],
            gettext("Gen type"): [self.gen_type],
            gettext("Selection type"): [self.selection_type],
            gettext("Selection rate"): [f"{int(self.selection_rate * 100)}%"],
            gettext("Crossover type"): [self.crossover_type],
            gettext("Mutation type"): [self.mutation_type],
            gettext("Mutation rate"): [f"{int(self.mutation_rate * 100)}%"],
            gettext("Elite population rate"): [f"{int(self.elite_pop_rate * 100)}%"],
        }

        exec_data = {
            gettext("Generation"): generations,
            gettext("Initial population"): initial_pops,
            gettext("Selected population"): selected_pops,
            gettext("Crossover population"): crossover_pops,
            gettext("Mutated population"): mutated_pops,
            gettext("Evaluated population"): evaluated_pops,
        }

        return config, exec_data

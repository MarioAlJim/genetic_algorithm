from src.controllers.playground_controller import PlaygroundController
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class TestPlaygroundController:
    def test_create_report(self):
        """Test create_report method"""
        controller = PlaygroundController()
        ga = GeneticAlgorithm()
        ga.num_generations = 10
        ga.init_pop()
        report = ga.execute()
        controller.create_report(report)
        assert True

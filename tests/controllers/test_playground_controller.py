from src.controllers.playground_controller import PlaygroundController
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class TestPlaygroundController:
    def test_create_report(self):
        """Test create_report method"""
        controller = PlaygroundController()
        ga = GeneticAlgorithm()
        ga.num_generations = 10
        report = ga.execute()
        controller.create_report(report)
        assert True

    def test_set_algorithm_parameters(self):
        """Test set_algorithm_parameters method"""
        controller = PlaygroundController()
        population_size = 2
        generations = 5
        selection_type = "random"
        selection_rate = 0.5
        crossover_type = "one-point"
        mutation_type = "random-resetting"
        mutation_rate = 0.3
        elitism_rate = 0.3

        conf = {
            "population_size": population_size,
            "generations": generations,
            "selection_type": selection_type,
            "selection_rate": selection_rate,
            "crossover_type": crossover_type,
            "mutation_type": mutation_type,
            "mutation_rate": mutation_rate,
            "elitism_rate": elitism_rate,
        }

        controller.set_algorithm_parameters(conf)
        config, exec_data = controller.start_execution()
        print ("Resultado de la ejecución:", exec_data["Evaluated population"])
        assert exec_data is not None

    def test_start_execution(self):
        """Test start_execution method"""
        controller = PlaygroundController()
        controller.algorithm.pop_size = 4
        controller.algorithm.num_generations = 2
        result = controller.start_execution()
        print(result)
        assert result is not None

    def test_evaluate_coverage(self):
        """Test evaluate_coverage method"""
        controller = PlaygroundController()
        test_data = ['[[-46.9541941616012, -93.57802221086277, -71.30467083937347], 0]\n[[54.68128573733085, -36.12361678585052, -71.30467083937347], 0]\n[[-61.65260698704449, -29.805818509778575, 10.558547207908248], 0]\n[[54.68128573733085, -80.83382766253064, 59.50730844526396], 0]\n[[-80.20186535685983, -29.805818509778575, 59.50730844526396], 0]',
                     '[[33.168365555976095, -29.805818509778575, 59.50730844526396], 0]\n[[-61.65260698704449, -29.805818509778575, 58.59918658337142], 0]\n[[-80.20186535685983, 37.240118702340396, 67.1597840098521], 0]\n[[-17.62334946642477, -29.805818509778575, 10.558547207908248], 0]\n[[-61.65260698704449, -35.35619563298012, -84.91049827242412], 0]']
        result = controller.evaluate_coverage(test_data)
        print("Resultado de la evaluación de cobertura:", result)
        assert result is not None

    def test_create_report_2(self):
        """Test create_report method"""
        content = [
            {
                'iteration': 1,
                'config_html': '<p>Configuración 1</p>',
                'exec_data_html': '<p>Datos de ejecución 1</p>',
                'graph': 'data:image/png;base64,XYZ...'
            },
            {
                'iteration': 2,
                'config_html': '<p>Configuración 2</p>',
                'exec_data_html': '<p>Datos de ejecución 2</p>',
                'graph': 'data:image/png;base64,ABC...'
            }
        ]

        controller = PlaygroundController()
        ga = GeneticAlgorithm()
        ga.num_generations = 5

        controller.create_report((content, 56))
        assert True

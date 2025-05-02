import coverage

def get_coverage(target_function, input_list):
    """
    Ejecuta una función con una lista de entradas mientras mide cobertura real.

    Args:
        target_function (callable): Función que será probada.
        input_list (list): Lista de entradas (tu población).

    Returns:
        dict: Resumen con líneas cubiertas y porcentaje de cobertura.
    """
    cov = coverage.Coverage()
    cov.start()

    for args in input_list:
        try:
            target_function(*args)
        except Exception as e:
            print(f"Error with input {args}: {e}")

    cov.stop()
    cov.save()

    summary = {}
    total_lines = 0
    total_covered = 0

    for filename in cov.get_data().measured_files():
        analysis = cov.analysis2(filename)
        statements = analysis[1]  # Todas las líneas que deberían ejecutarse
        missing = analysis[3]     # Las que no se ejecutaron

        num_statements = len(statements)
        num_missing = len(missing)
        num_covered = num_statements - num_missing

        summary[filename] = {
            'total_statements': num_statements,
            'executed_statements': num_covered,
            'missing_statements': missing
        }

        total_lines += num_statements
        total_covered += num_covered

    percent_covered = (total_covered / total_lines * 100) if total_lines else 0

    return {
        'coverage_summary': summary,
        'coverage_percent': percent_covered
    }


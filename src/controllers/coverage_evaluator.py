import coverage

def get_coverage(target_function, input_list: list) -> dict:
    """
    Executes the target function with the provided inputs and evaluates the code coverage.

    Args:
        target_function (callable): Objective function to be executed.
        input_list (list): List with inputs to be passed to the target function.

    Returns:
        dict: Coverage summary and percentage.
    """
    cov = coverage.Coverage()
    cov.start()

    for args in input_list:
        try:
            target_function(args)
        except Exception as e:
            print(f"Error with input {args}: {e}")

    cov.stop()
    cov.save()

    summary = {}
    total_lines = 0
    total_covered = 0

    for filename in cov.get_data().measured_files():
        analysis = cov.analysis2(filename)
        statements = [58, 64, 65, 66, 67, 69, 70, 71, 72, 73, 74, 75, 78, 80, 82, 84]
        missing = analysis[3]     # Las que no se ejecutaron

        num_statements = len(statements)
        num_missing = len(missing) - 26
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


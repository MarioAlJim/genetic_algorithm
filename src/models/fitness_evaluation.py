"""This file is for defining the fitness functions.

1. Evaluates the chromosome.
2. Returns a list with the chromosome and its fitness score.
    I.E. for the score of triangle classification problem
    Chromosome input: [3,3,3]
    Expected solution input: Equilateral
    Fitness function output: [[3,3,3], 0]
"""
def classify_triangle(chromosome: list):
    """Classifies the triangle"""
    classification = None
    a = chromosome[0]
    b = chromosome[1]
    c = chromosome[2]

    if a > 0 and b > 0 and c > 0:
        if a+b > c and b+c > a and c+a > b:
            if a != b and b != c and c != a:
                classification = 'scalene'
            elif a == b == c:
                classification = 'equilateral'
            elif ((a == b != c) or
                  (a == c != b) or
                  (b == c != a)):
                classification = 'isosceles'
        else:
            classification = 'invalid'
    else:
        classification = 'out of range'

    return classification

def score_triangle_classification(chromosome: list, expected_solution):
    """Fitness function for triangle classification problem"""
    difference = 0

    solution = classify_triangle(chromosome)

    if solution != expected_solution:
        difference = 1

    return [chromosome, difference]

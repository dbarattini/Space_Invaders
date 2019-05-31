import pytest
from ga.ga import *


@pytest.fixture
def binary_chromosome1():
    """Returns a Chromosome instance with binary genes"""
    c = Chromosome([1, 1, 1, 1, 1])
    c.calculate_fitness(fitness_function)
    return c


@pytest.fixture
def binary_chromosome2():
    """Returns a Chromosome instance with binary genes"""
    c = Chromosome([0, 0, 0, 0, 0])
    c.calculate_fitness(fitness_function)
    return c


def fitness_function(genes):
    fitness = 0
    for gene in genes:
        fitness += gene
    return fitness


@pytest.fixture
def binary_pop_with_fitness():
    c1 = Chromosome([1, 1, 1, 1, 1])
    c2 = Chromosome([0, 0, 0, 0, 0])
    pop = [c1, c2]

    for c in pop:
        c.calculate_fitness(fitness_function)

    return pop


def test_tournament_selection(binary_pop_with_fitness, binary_chromosome1, binary_chromosome2):
    parents = tournament_selection(binary_pop_with_fitness)
    assert len(parents) == 2
    assert parents[0] == binary_chromosome1 or parents[0] == binary_chromosome2
    assert parents[1] == binary_chromosome1 or parents[1] == binary_chromosome2


def test_two_points_crossover(binary_pop_with_fitness, binary_chromosome1):
    offspring = two_points_crossover(binary_pop_with_fitness)
    assert len(offspring) == 2
    assert len(offspring[0].genes) == len(binary_chromosome1.genes) and len(offspring[1].genes) == len(
        binary_chromosome1.genes)

import pytest
from ga.ga_actors import *


@pytest.fixture
def binary_gene():
    """Returns a Gene instance with binary alleles"""
    return Gene([0, 1])


@pytest.fixture
def string_gene():
    """Returns a Gene instance with string alleles"""
    return Gene(["a", "b", "c"])


@pytest.fixture
def binary_chromosome():
    """Returns a Chromosome instance with binary genes"""
    return Chromosome([0, 1, 0, 0, 1])


@pytest.fixture
def string_chromosome():
    """Returns a Chromosome instance with string genes"""
    return Chromosome(["a", "b", "c", "a", "a", "c"])


def test_chromosome_initialization(binary_chromosome):
    assert binary_chromosome.genes == [0, 1, 0, 0, 1]


def fitness_function(genes):
    fitness = 0
    for gene in genes:
        fitness += gene
    return fitness


def test_binary_chromosome_calculate_fitness(binary_chromosome):
    binary_chromosome.calculate_fitness(fitness_function)
    assert binary_chromosome.fitness == 2


def fitness_function2(genes):
    fitness = 0
    for gene in genes:
        if gene == "a":
            fitness += 3
        elif gene == "b":
            fitness += 2
        else:
            fitness += 1
    return fitness


def test_string_chromosome_calculate_fitness(string_chromosome):
    string_chromosome.calculate_fitness(fitness_function2)
    assert string_chromosome.fitness == 13



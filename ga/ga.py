import random
import sys

from ga.ga_actors import *
import numpy
import math
from typing import Callable, List, Tuple, Dict
import matplotlib.pyplot as plt
from collections import OrderedDict
from statistics import mean


WEIGHTS = [0.02, 0.02, 0.96]


def generate_pop_zero(gene_prototype: Gene, n_genes: int, pop_size: int) -> List[Chromosome]:
    """ Generate the first population

    :param gene_prototype: a prototype of a Gene
    :param n_genes: number of genes generated for each Chromosome
    :param pop_size: number of Chromosomes within the population
    :return: population zero
    """
    random.seed()
    pop = []

    for i in range(0, pop_size):
        pop.append(Chromosome(random.choices(gene_prototype.alleles, k=n_genes)))
    return pop


def generate_pop_zero_with_weights(gene_prototype: Gene, n_genes: int, pop_size: int, weights: List[float]) -> \
        List[Chromosome]:
    """ Generate the first population based on weights

    :param weights: list containing the probability that an allele is chosen ordered like alleles
    :param gene_prototype: a prototype of a Gene
    :param n_genes: number of genes generated for each Chromosome
    :param pop_size: number of Chromosomes within the population
    :return: population zero
    """
    random.seed()
    pop = []

    for i in range(0, pop_size):
        pop.append(Chromosome(random.choices(gene_prototype.alleles, k=n_genes, weights=weights)))
    return pop


def calculate_pop_fitness(pop: List[Chromosome],
                          fitness_function: Callable[[List[Gene]], int] = lambda g: sum(g)) -> Tuple:
    """ Calculates and updates the fitness of all the chromosomes of a population and returns the best chromosome and a
    list containing all the fitnesses

    :param pop: population
    :param fitness_function: fitness function
    :return: A tuple containing the Chromosome with highest fitness and a list containing all the population fitnesses
    """
    best_chromosome = None
    fitnesses = []
    for chromosome in pop:
        chromosome.calculate_fitness(fitness_function)
        fitnesses.append(chromosome.fitness)
        if best_chromosome is None or best_chromosome.fitness < chromosome.fitness:
            best_chromosome = chromosome
    return best_chromosome, fitnesses


def __media_weights_calculator(pop: List[Chromosome]) -> List[float]:
    """ Calculates for every Chromosome in a population the probability to be chosen proportionally to their fitness

    :param pop: population
    :return: weights list ordered like the pop list
    """
    total_fitness = 0
    weights = []
    for c in pop:
        total_fitness += c.fitness
    for c in pop:
        weights.append(c.fitness / total_fitness)
    return weights


def roulette_wheel_selection(pop: List[Chromosome]) -> List[Chromosome]:
    """ Select two parents within the population based on the weights generated by the weights_calculator.

    :param pop: population
    :return: selected parents
    """
    weights = __media_weights_calculator(pop)
    parents = numpy.random.choice(pop, 2, p=weights)
    return parents


def tournament_selection(pop: List[Chromosome]) -> List[Chromosome]:
    """ Select two parents within the population based on tournament selection.

    :param pop: population
    :return: selected parents
    """
    parents = []
    k = 0.75
    for i in range(0, 2):
        contendents = list(numpy.random.choice(pop, 2))
        contendents.sort(key=lambda x: x.fitness, reverse=True)
        r = random.uniform(0, 1)
        if r < k:
            parents.append(contendents[0])
        else:
            parents.append(contendents[1])
    return parents


def single_point_crossover(parents: List[Chromosome], probability: float = 0.7) -> List[Chromosome]:
    """ Make the crossover of two parents to generate two child.
    The crossover has a probability to be made.
    The crossover point is random.

    :param parents: selected parents
    :param probability: probability that the crossover is made
    :return: offspring
    """
    cut_point = random.randint(1, len(parents[1].genes) - 1)
    if random.random() < probability:
        first_child = Chromosome(parents[0].genes[:cut_point] + parents[1].genes[cut_point:])
        second_child = Chromosome(parents[1].genes[:cut_point] + parents[0].genes[cut_point:])
    else:
        first_child = Chromosome(parents[0].genes.copy())
        second_child = Chromosome(parents[1].genes.copy())
    return [first_child, second_child]


def two_points_crossover(parents: List[Chromosome], probability: float = 0.7) -> List[Chromosome]:
    """ Make a two points crossover of two parents to generate two child.
    The crossover has a probability to be made.
    The crossover points are random.

    :param parents: selected parents
    :param probability: probability that crossover is made
    :return: offspring
    """
    cut_points = numpy.random.randint(0, len(parents[1].genes), size=2)
    cut_points.sort()
    if random.random() < probability:
        first_child = Chromosome(parents[0].genes[:cut_points[0]] + parents[1].genes[cut_points[0]:cut_points[1]] +
                                 parents[0].genes[cut_points[1]:])
        second_child = Chromosome(parents[1].genes[:cut_points[0]] + parents[0].genes[cut_points[0]:cut_points[1]] +
                                  parents[1].genes[cut_points[1]:])
    else:
        first_child = Chromosome(parents[0].genes.copy())
        second_child = Chromosome(parents[1].genes.copy())
    return [first_child, second_child]


def mutation(child: Chromosome, gene_prototype, mutation_function: Callable[[Gene], Gene], probability: float = 0.001) -> None:
    """ Perform the mutation of the child.
    Each gene has a probability of being mutated.

    :param gene_prototype: used to get all the alleles
    :param child: Chromosome to be mutated
    :param mutation_function: given a gene returns its mutation
    :param probability: probability that a gene is mutated
    """
    for i, gene in enumerate(child.genes):
        if random.random() < probability:
            child.genes[i] = mutation_function(gene_prototype)


def ga(gene_prototype: Gene, n_genes: int, pop_size: int, mutation_function: Callable[[Gene], Gene],
        n_generations: int, fitness_function: Callable[[List[Gene]], int] = lambda g: sum(g),
        pc: float = 0.7, pm: float = 0.001, max_fitness: float = math.inf, elitism: int = 0,
        selection_function=roulette_wheel_selection, crossover_function=single_point_crossover) -> Dict:
    """ Perform a Genetic Algorithm

    :param crossover_function: function used to make crossover
    :param selection_function: function used to choose two parents
    :param elitism: pop to save in next gen (percentage)
    :param max_fitness: fitness to achieve
    :param gene_prototype: a prototype of a Gene
    :param n_genes: number of genes generated for each Chromosome
    :param pop_size: number of Chromosomes within the population
    :param mutation_function: given a gene returns its mutation
    :param n_generations: number of max generation
    :param fitness_function: fitness function
    :param pc: crossover probability
    :param pm: mutation probability
    """

    if ((pop_size - int((pop_size * elitism) / 100)) % 2) != 0:
        sys.exit("Error: change the elitism value to keep the population size fixed "
                 "[ pop_size - int((pop_size * elitism)/100) must be even ]")
    gen = 0
    results = OrderedDict()
    pop = generate_pop_zero_with_weights(gene_prototype, n_genes, pop_size, WEIGHTS)
    #pop = generate_pop_zero(gene_prototype, n_genes, pop_size)
    best_chromosome, fitnesses = calculate_pop_fitness(pop, fitness_function)
    avg_fitness = round(mean(fitnesses), 2)
    best_chromosome_copy = Chromosome(best_chromosome.genes)
    best_chromosome_copy.fitness = best_chromosome.fitness
    results["gen0"] = {"gen": 0, "best": best_chromosome_copy, "fitnesses": fitnesses, "avg": avg_fitness}
    print("best of generation", gen, best_chromosome)
    for i in range(0, n_generations):
        if max_fitness <= best_chromosome.fitness:
            break
        gen += 1
        pop.sort(key=lambda x: x.fitness, reverse=True)
        new_pop = pop[: int((pop_size * elitism) / 100)]
        limit = pop_size - len(new_pop)
        for j in range(0, int(limit / 2)):
            parents = selection_function(pop)
            offspring = crossover_function(parents, pc)
            mutation(offspring[0], gene_prototype, mutation_function, pm)
            mutation(offspring[1], gene_prototype, mutation_function, pm)
            new_pop.extend(offspring)
        pop = new_pop
        best_chromosome, fitnesses = calculate_pop_fitness(pop, fitness_function)
        avg_fitness = round(mean(fitnesses), 2)
        best_chromosome_copy = Chromosome(best_chromosome.genes)
        best_chromosome_copy.fitness = best_chromosome.fitness
        results["gen" + str(gen)] = {"gen": gen, "best": best_chromosome_copy, "fitnesses": fitnesses, "avg": avg_fitness}
        print("best of generation", i + 1, best_chromosome)
    return results


def plot_best_fitnesses(results: Dict) -> None:
    """ Plots the best chromosomes of each generation

    :param results: results of a ga algorithm
    """
    bests = []
    last_gen_key = list(results.keys())[-1]
    for key, val in results.items():
        bests.append(val["best"].fitness)

    plt.plot([i for i in range(results[last_gen_key]["gen"] + 1)], bests, label="best")
    plt.xlabel('generation')
    plt.ylabel('best individual')
    plt.show()


def plot_results(results: Dict) -> None:
    """ Plots the genetic algorithm's results (best chromosome and average fitness of each generation)

    :param results: results of a ga algorithm
    """
    bests = []
    avgs = []
    last_gen_key = list(results.keys())[-1]
    for key, val in results.items():
        bests.append(val["best"].fitness)
        avgs.append(val["avg"])

    plt.plot([i for i in range(results[last_gen_key]["gen"] + 1)], bests, 'b', label="best")
    plt.plot([i for i in range(results[last_gen_key]["gen"] + 1)], avgs, 'r', label="averages")
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.legend()
    plt.show()
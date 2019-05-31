import numpy

from ga.ga_actors import Gene, Chromosome
from ga.ga import ga, tournament_selection, plot_best_fitnesses, plot_results, roulette_wheel_selection
import random
from spaceinvaders import play


gene_prototype = Gene(["move-right", "move-left", "shoot"])
n_genes_considered = 5000
pop_size = 20
individual_index = 0
gen = 0
wins = 0


def fitness_function(moves):
    global individual_index
    global gen
    global wins

    individual_index += 1

    fitness1, wins = play(moves, n_genes_considered, gen, individual_index, wins)
    fitness2, wins = play(moves, n_genes_considered, gen, individual_index, wins)
    fitness3, wins = play(moves, n_genes_considered, gen, individual_index, wins)
    # fitness4, wins = play(moves, n_genes_considered, gen, individual_counter, wins)
    # fitness5, wins = play(moves, n_genes_considered, gen, individual_counter, wins)

    fitness = round((fitness1 + fitness2 + fitness3) / 3, 2)
    print("fitness:", fitness)
    if individual_index == pop_size:
        gen += 1
        individual_index = 0
    if fitness >= 0:
        return fitness
    else:
        return 0


def one_point_cf(parents, probability):
    global n_genes_considered

    if n_genes_considered > (len(parents[1].genes) - 1):
        limit = len(parents[1].genes) - 1
    else:
        limit = n_genes_considered

    cut_point = random.randint(1, limit)

    if random.random() < probability:
        first_child = Chromosome(parents[0].genes[:cut_point] + parents[1].genes[cut_point:])
        second_child = Chromosome(parents[1].genes[:cut_point] + parents[0].genes[cut_point:])
    else:
        first_child = Chromosome(parents[0].genes.copy())
        second_child = Chromosome(parents[1].genes.copy())
    return [first_child, second_child]


def two_points_cf(parents, probability):
    global n_genes_considered

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


results = ga(gene_prototype=gene_prototype, n_genes=5000, pop_size=pop_size, mutation_function=lambda x: random.choice(x.alleles),
             n_generations=30, fitness_function=fitness_function, elitism=10, crossover_function=two_points_cf,
             selection_function=tournament_selection, pc=0.7, pm=0.01)

print(results)

plot_best_fitnesses(results)
plot_results(results)





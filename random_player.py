from simple_ga.ga_actors import Gene, Chromosome
from simple_ga.sga import sga
import random
from spaceinvaders import play


gene_prototype = Gene(["move-right", "move-left", "shoot"])
n_genes_considered = 5000
individual_counter = 0
pop_size = 50
gen = 0
wins = 0


def ff(moves):
    global individual_counter
    global gen
    global wins

    individual_counter += 1
    fitness, wins = play(moves, n_genes_considered, gen, individual_counter, wins)

    print("fitness:", fitness)
    if individual_counter == pop_size:
        gen += 1
        individual_counter = 0
    if fitness >= 0:
        return 0
    else:
        return 0


def cf(parents, probability):
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


sga(gene_prototype=gene_prototype, n_genes=5000, pop_size=pop_size, mutation_function=lambda x: random.choice(x.alleles),
    n_generations=100, fitness_function=ff, elitism=4, crossover_function=cf)

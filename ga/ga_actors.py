from typing import Any, List, Callable


class Gene(object):
    """Elementary object.
    Contains all its possible values (an alleles list)
    """
    def __init__(self, alleles: List[Any]) -> None:
        """

        :param alleles: list of all possible Gene values
        """
        self.alleles = alleles

    def __repr__(self):
        """ Human representation of a gene

        """
        return repr(self.alleles)


class Chromosome(object):
    """Representation of an individual/solution.
    It's a composition of genes (list) and memorizes its fitness.
    """
    def __init__(self, genes: List[Gene]) -> None:
        """

        :param genes: list of genes that made the chromosome
        """
        self.genes = genes
        self.fitness = 0

    def __repr__(self):
        """ Human representation of a chromosome

        """
        return repr((self.fitness, self.genes))

    def __eq__(self, other):
        if not isinstance(other, Chromosome):
            return False
        else:
            return self.genes == other.genes and self.fitness == other.fitness

    def calculate_fitness(self, fitness_function: Callable[[List[Gene]], float]) -> None:
        """ Calculate the fitness and update the fitness value

        :param fitness_function: functions that evaluate the genes and returns a value
        """
        self.fitness = fitness_function(self.genes)

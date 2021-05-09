import numpy


def genetic_crossover(genes_parent1, genes_parent2, n_children, p_crossover=0.5, p_mutation=0.2):

    n_genes = len(genes_parent1)
    children = []

    for j in range(n_children):
        crossover_indexes = numpy.random.binomial(1, p_crossover, n_genes)
        mutation = numpy.random.binomial(1, p_mutation, n_genes) * numpy.random.normal(size=n_genes)
        crossover = (
            crossover_indexes * genes_parent1
            + (numpy.ones(n_genes) - crossover_indexes) * genes_parent2
            + mutation
        )
        children.append(crossover)

    return children

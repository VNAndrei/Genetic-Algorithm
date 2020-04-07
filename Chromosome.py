import numpy as np


class Chromosome:
    def __init__(self, chromosomeParameters):
        self.__chromosomeParameters = chromosomeParameters
        self.__genes = self.__chromosomeParameters["initializeGeneFunction"](self.__chromosomeParameters)
        self.__fitness = 0.0

    @property
    def genes(self):
        return self.__genes

    @genes.setter
    def genes(self, newGenes=[]):
        self.__genes = newGenes

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, newFitness):
        self.__fitness = newFitness

    def crossover(self, chromosome, probability):
        decision = np.random.choice([True, False], 1, [probability, 1 - probability])

        if decision[0]:
            return self.__chromosomeParameters["crossoverFunction"](self, chromosome, self.__chromosomeParameters)
        if self.fitness > chromosome.fitness:
            return self.__copy__()
        return chromosome.__copy__()

    def mutation(self, probability):
        decision = np.random.choice([True, False], 1, [probability, 1 - probability])
        if decision[0]:
            return self.__chromosomeParameters["mutationFunction"](self, self.__chromosomeParameters)

    def __eq__(self, other):
        return self.__genes == other.__genes and self.__fitness == other.__fitness

    def __str__(self):
        return str(self.__genes)

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        cr = Chromosome(self.__chromosomeParameters)
        cr.__genes = self.__genes.copy()
        cr.__fitness = self.__fitness
        return cr

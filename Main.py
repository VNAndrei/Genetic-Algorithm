import random
from math import sqrt

from Chromosome import Chromosome
from GeneticAlgorithm import GeneticAlgorithm

def readInput(fisier):
    parameters = {}
    with open(fisier, 'r') as file:
        n = int(file.readline())
        domain = [[int(num) for num in line.split(',')] for line in file]
        parameters["chromosomeSize"] = n
        parameters["domain"] = domain
    return parameters


def fitness(cities, algorithmParameters):

    adjacencyMatrix = algorithmParameters["domain"]


    distance = 0
    for i in range(0, len(cities) - 1):
        distance += adjacencyMatrix[cities[i] - 1][cities[i + 1] - 1]
    distance += adjacencyMatrix[cities[len(cities) - 1] - 1][cities[0] - 1]

    return 1 / distance


def generateShuffle(chromosomeParameters):
    n = chromosomeParameters["chromosomeSize"]
    perm = [i for i in range(1, n + 1)]
    random.shuffle(perm)
    return perm


def crossover(c1, c2, chromosomeParameters):
    firstCut = random.randint(0, chromosomeParameters["chromosomeSize"]-1)
    secondCut = random.randint(0, chromosomeParameters["chromosomeSize"]-1)
    if firstCut > secondCut:
        firstCut, secondCut = secondCut, firstCut

    firstParentGenes = c1.genes[firstCut:secondCut]

    secondParentGenes = []
    for i in range(0, chromosomeParameters["chromosomeSize"]):
        if c2.genes[i] not in firstParentGenes:
            secondParentGenes.append(c2.genes[i])

    newGenes = secondParentGenes[chromosomeParameters["chromosomeSize"] - secondCut:] \
               + firstParentGenes \
               + secondParentGenes[0:chromosomeParameters["chromosomeSize"] - secondCut]

    offspring = Chromosome(chromosomeParameters)
    offspring.genes = newGenes.copy()

    return offspring

def crossover2(c1, c2, chromosomeParameters):
    firstCut = random.randint(0, chromosomeParameters["chromosomeSize"]-1)
    secondCut = random.randint(0, chromosomeParameters["chromosomeSize"]-1)
    if firstCut > secondCut:
        firstCut, secondCut = secondCut, firstCut

    firstParentGenes = c1.genes[firstCut:secondCut]

    secondParentGenes = []
    for i in range(0, chromosomeParameters["chromosomeSize"]):
        if c2.genes[i] not in firstParentGenes:
            secondParentGenes.append(c2.genes[i])

    newGenes = secondParentGenes[0:firstCut]+\
                firstParentGenes +\
        secondParentGenes[firstCut:]
    offspring = Chromosome(chromosomeParameters)
    offspring.genes = newGenes.copy()

    return offspring

def mutation2(chromosome,chromosomeParameters):

    pos1 = random.randint(0, chromosomeParameters["chromosomeSize"] - 1)
    pos2 = random.randint(0, chromosomeParameters["chromosomeSize"] - 1)
    if pos2 < pos1:
        pos1, pos2 = pos2, pos1
    chromosome.genes[pos1:pos2] = chromosome.genes[pos1:pos2][::-1]



def mutation(chromosome, chromosomeParameters):
    pos1 = random.randint(0, chromosomeParameters["chromosomeSize"] - 1)
    pos2 = random.randint(0, chromosomeParameters["chromosomeSize"] - 1)

    if pos2 < pos1:
        pos1, pos2 = pos2, pos1
    el = chromosome.genes[pos2]
    del chromosome.genes[pos2]
    chromosome.genes.insert(pos1 + 1, el)


def main():
    parameters = readInput("data/mediumF.txt")
    chromosomeParameters = {}

    chromosomeParameters["crossoverFunction"] = crossover2
    chromosomeParameters["mutationFunction"] = mutation2
    chromosomeParameters["initializeGeneFunction"] = generateShuffle
    chromosomeParameters["chromosomeSize"] = parameters["chromosomeSize"]

    algorithmParameters = {}
    algorithmParameters["domain"] = parameters["domain"]
    algorithmParameters["selectionFunction"] = GeneticAlgorithm.tournamentSelection
    algorithmParameters["populationSize"] = 300
    algorithmParameters["numberOfGenerations"] = 10000
    algorithmParameters["fitnessFunction"] = fitness
    algorithmParameters["k"] = 30
    algorithmParameters["trunc"] = 0.1
    algorithmParameters["crossoverProbability"] = 1
    algorithmParameters["mutationProbability"] = 0.3
    algorithmParameters["newGenerationFunction"] = GeneticAlgorithm.newGenerationSteadyState

    geneticAlgorithm = GeneticAlgorithm(algorithmParameters)

    geneticAlgorithm.initialization(chromosomeParameters)
    geneticAlgorithm.evaluation()
    geneticAlgorithm.run()





main()
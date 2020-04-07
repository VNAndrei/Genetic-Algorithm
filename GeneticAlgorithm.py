from Chromosome import Chromosome
import random


class GeneticAlgorithm:
    def __init__(self, algorithmParameters):
        self.__algorithmParameters = algorithmParameters
        self.__population = []

    @property
    def population(self):
        return self.__population

    @population.setter
    def population(self, newPopulation):
        self.__population = newPopulation

    def initialization(self, chromosomeParameters):
        for _ in range(0, self.__algorithmParameters["populationSize"]):
            chromosome = Chromosome(chromosomeParameters)
            self.__population.append(chromosome)

    def evaluation(self):
        for chromosome in self.__population:
            chromosome.fitness = self.__algorithmParameters["fitnessFunction"](chromosome.genes,
                                                                               self.__algorithmParameters)

    def bestChromosome(self):
        best = self.__population[0]
        for chromosome in self.__population:
            if chromosome.fitness > best.fitness:
                best = chromosome
        return best

    def worstChromosome(self):
        worst = self.__population[0]
        for chromosome in self.__population:
            if chromosome.fitness < worst.fitness:
                worst = chromosome
        return worst

    def randomSelection(self):
        randomPosition1 = random.randint(0, self.__algorithmParameters["populationSize"] - 1)
        randomPosition2 = random.randint(0, self.__algorithmParameters["populationSize"] - 1)
        if self.__population[randomPosition1].fitness > self.__population[randomPosition2].fitness:
            return self.__population[randomPosition1]
        return self.__population[randomPosition1]

    def rouletteSelection(self):
        fitnessSum = sum([chromosome.fitness for chromosome in self.population])
        pick = random.uniform(0, fitnessSum)
        current = 0
        for chromosome in self.__population:
            current += chromosome.fitness
            if current > pick:
                return chromosome

    def tournamentSelection(self):
        bestParents = random.choices(range(0, self.__algorithmParameters["populationSize"]),
                                     k=self.__algorithmParameters["k"])
        best = self.__population[bestParents[0]]
        for parent in bestParents:
            if self.__population[parent].fitness > best.fitness:
                best = self.__population[parent]
        return best

    def truncationSelection(self):
        self.__population.sort(reverse=True, key=lambda chromosome: chromosome.fitness)
        numberOfParents = self.__algorithmParameters["populationSize"]*self.__algorithmParameters["trunc"]
        return self.__population[0:int(numberOfParents)],

    def newGenerationTruncation(self):
        parents = self.truncationSelection()
        newPopulation = [] + parents
        while len(newPopulation) != self.__algorithmParameters["populationSize"]:
            fistParent = random.choice(self.__population)
            secondParent = random.choice(self.__population)
            offspring = fistParent.crossover(secondParent, self.__algorithmParameters["crossoverProbability"])
            offspring.mutation(self.__algorithmParameters["mutationProbability"])
            newPopulation.append(offspring)

        self.__population = newPopulation
        self.evaluation()

    def newGeneration(self):
        newPopulation = []
        for _ in range(0, self.__algorithmParameters["populationSize"]):
            firstParent = self.__algorithmParameters["selectionFunction"](self)
            secondParent = self.__algorithmParameters["selectionFunction"](self)
            offspring = firstParent.crossover(secondParent, self.__algorithmParameters["crossoverProbability"])
            offspring.mutation(self.__algorithmParameters["mutationProbability"])
            newPopulation.append(offspring)

        self.__population = newPopulation
        self.evaluation()

    def newGenerationElitism(self):
        newPopulation = [self.bestChromosome()]
        for _ in range(1, self.__algorithmParameters["populationSize"]):
            firstParent = self.__algorithmParameters["selectionFunction"](self)
            secondParent = self.__algorithmParameters["selectionFunction"](self)
            offspring = firstParent.crossover(secondParent, self.__algorithmParameters["crossoverProbability"])
            offspring.mutation(self.__algorithmParameters["mutationProbability"])
            newPopulation.append(offspring)

        self.__population = newPopulation
        self.evaluation()

    def newGenerationSteadyState(self):

        for _ in range(0, self.__algorithmParameters["populationSize"]):
            firstParent = self.__algorithmParameters["selectionFunction"](self)
            secondParent = self.__algorithmParameters["selectionFunction"](self)

            offspring = firstParent.crossover(secondParent, self.__algorithmParameters["crossoverProbability"])
            offspring.mutation(self.__algorithmParameters["mutationProbability"])

            offspring.fitness = self.__algorithmParameters["fitnessFunction"](offspring.genes.copy(),
                                                                              self.__algorithmParameters)

            worst = self.worstChromosome()

        if offspring.fitness > worst.fitness:
            self.__population.remove(worst)
            self.__population.append(offspring)

    def run(self):
        globalBest = self.bestChromosome().fitness
        for i in range(1, self.__algorithmParameters["numberOfGenerations"] + 1):
            self.__algorithmParameters["newGenerationFunction"](self)
            best = self.bestChromosome()
            if best.fitness > globalBest:
                globalBest = best.fitness
            avg = 0

            for j in self.__population:
                avg += j.fitness

            avrg= 1 / (avg / self.__algorithmParameters["populationSize"])
            print("generation:" + str(i))

            print("avg: " + str(avrg))
            print("global: " + str(1 / globalBest))
            print("\n")
            if int(avrg) == int(globalBest):
                break

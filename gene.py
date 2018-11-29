#This project has implemented the use of matplotlib to graph the data
#If it is desired and matplotlib and numpy is intalled, uncommenting the required lines
#Can be done at line: 8,9, 106 and 209-225



import random
#import matplotlib.pyplot as plt
#import numpy as np
import math

max, min = 11, 22


data=open("data1.txt", "r") #For dataset 2 change data1.txt to data2.txt
rules = data.readlines()
number_of_rules=32         #For dataset1: number_of_rules = 32 - for dataset2 change to 64
rule_length = 6           #For dataset1: rule_length = 6 - for dataset2 change to 8
number_rules = 10
class Rule(object):
    def __init__(self, condition, output):

        self.condition = condition
        self.output = output
        self.matches = 0

    def __repr__(self):
        return ("(%r, %r)" %(self.condition, self.output))


class Individual(object):

    genelength = 60         #For dataset1: lengthL 60 - fir dataset2: change to 80
    separator = ''
    optimization = min

    def __init__(self, chromosome=None):
        self.chromosome = chromosome or self._makechromosome()
        self.score = 0  # set during evaluation

    def _makechromosome(self):

        return [random.choice([0,1]) for gene in range(self.genelength)]


    def crossover(self, other):
        left = random.randrange(1, self.genelength - 2)
        right = random.randrange(left, self.genelength - 1)

        def mate(p0, p1):
            chromosome = p0.chromosome[:]
            chromosome[left:right] = p1.chromosome[left:right]
            child = p0.__class__(chromosome)
            return child

        return mate(self, other), mate(other, self)


    def __repr__(self):
        "returns string representation of self"
        return 'chromosome="%s" fitness=%s' % \
               (self.separator.join(map(str, self.chromosome)), self.score)

    def __cmp__(self, other):
        if self.optimization == min:
            return cmp(self.score, other.score)
        else:  # MAXIMIZE
            return cmp(other.score, self.score)

    def copy_chromosome(self):
        copy_chromosome = self.__class__(self.chromosome[:])
        copy_chromosome.score = self.score
        return copy_chromosome


class Population(object):
    def __init__(self, kind, population=None, size=100, maxgenerations=200,
                 crossover_rate=0.70, mutation_rate=0.01, optimum=None):
        self.kind = kind
        rulebase = self.loadData()
        self.cleanPltData()
        self.size = size
        self.optimum = optimum
        self.population = population or self._makepopulation()
        for individual in self.population:
            individual.evaluate(individual.chromosome, rulebase, rule_length, number_of_rules, number_rules, individual.genelength)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.maxgenerations = maxgenerations
        self.gen = 0
        self.report()
        self.run(rulebase)

    # Return x amount of individuals in our population size
    def _makepopulation(self):
        return [self.kind() for individual in range(self.size)]

    # This function runs through the evolution process.

    def run(self, rulebase):
        while not self.gen > self.maxgenerations:
            self.population.sort()
            self.evolve(rulebase)
            self.gen += 1
            self.report()
        #self.pltData()

    # This loads the datasets into our class Rule.
    # We append the first bit before the space to the condition
    # and the bit after the space to the output/class
    def loadData(self):
        rulebase = []
        for i in range(1, number_of_rules + 1):
            string = rules[i].split(" ")
            condition = list(map(int, list(string[0])))
            classification = int(string[1][0])
            rulebase.append(Rule(condition, classification))
        return rulebase


    # This functions starts by taking a copy of the current population.
    # We do tournament selection
    # Crossover
    # And mutation for each individual in the next population
    # Nex step is to carry out fitness calculation - function name: evaluate
    # And at the end appends the new individuals to our population pool
    def evolve(self, rulebase):
        next_population = [self.best.copy_chromosome()]
        total_fitness= 0
        best_fitness = 0
        while len(next_population) < self.size:
            mate1 = self._tournament()
            if random.random() < self.crossover_rate:
                mate2 = self._tournament()
                offspring = mate1.crossover(mate2)
            else:
                offspring = [mate1.copy_chromosome()]
            for individual in offspring:
                self._mutate(individual, rule_length)
                individual.evaluate(individual.chromosome, rulebase, rule_length, number_of_rules, number_rules, individual.genelength)
                next_population.append(individual)
                total_fitness += individual.score
                if best_fitness < individual.score:
                    best_fitness = individual.score
        average_fitness = total_fitness / self.size
        print("Average Fitness: ", average_fitness)
        d=open('output2.txt', 'a')
        d.write(str(self.gen) + " " + str(best_fitness) + "\n")
        d.write(" \n")
        d.close
        f = open("output.txt", "a")
        f.write(str(self.gen) + " " + str(average_fitness) + "\n")
        f.write(" \n")
        f.close()

        #print("next population:", next_population)

        self.population = next_population[:self.size]

    def _mutate(self, individual, rule_length):
        for gene in range(individual.genelength):
            if random.random() < self.mutation_rate:
                individual.mutate(gene, rule_length)

    #
    # Tournament selection
    #
    def _tournament(self, size=100 , choosebest=0.70):
        competitors = [random.choice(self.population) for i in range(size)]
        competitors.sort()
        if random.random() < choosebest:
            return competitors[0]
        else:
            return random.choice(competitors[1:])

    def best():
        def fget(self):
            return self.population[0]

        return locals()

    best = property(**best())

    def report(self):
        print("!-----------------------------------------------------------------------------------------------!")
        print ("generation: ", self.gen)
        print("!-----------------------------------------------------------------------------------------------!")
        #self.population.sort()
        #for i in self.population:
        #    print(i)
        print("!-----------------------------------------------------------------------------------------------!")
        print ("best: ", self.best)


    # This function cleans out the data  in the 2 files

    def cleanPltData(self):
        f = open("output.txt", "r+")
        f.truncate(0)
        d = open("output2.txt", "r+")
        d.truncate(0)


    # Plots the data to a graph
    # data is the fitness average
    # data2 is the best fitness
    # both recorded for each generation

    #def pltData(self):
    #    data = np.loadtxt('output.txt')
    #    data2 = np.loadtxt('output2.txt')
        #plot the first column as x, and second column as y
    #    x = data[:, 0]
    #    y = data[:, 1]
    #    x1 = data2[:, 0]
    #    y2 = data2[:, 1]
        #(x,y,'ro') plot only points
    #    plt.plot(x, y, x1, y2)
    #    plt.xlabel('Generation')
    #    plt.ylabel('Fitness average')
        #set up max number of generations
    #    plt.xlim(0.0,200.)
        # set up max fitness value
    #    plt.ylim(0.0, 70.)
    #    plt.show()



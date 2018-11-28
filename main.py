

import gene
import random

class Init(gene.Individual):
    optimization = gene.max

    # evaluate/fitness function calculates the fitness
    # of each individual in the population.

    def evaluate(self, individual, rulebase, rule_length, number_of_rules, number_rules, length):
        ruleb = []
        self.score = 0

        for i in range(0, length, rule_length):
            string = individual[slice(i, i+rule_length, 1)]
            ruleb.append(gene.Rule(string[slice(0, rule_length-1)], string[rule_length-1]))
        print(ruleb)
        for i in range(number_of_rules):
            for k in range(number_rules):

                bit_matches = 0
                for l in range(rule_length - 1):

                    if ruleb[k].condition[l] == rulebase[i].condition[l] or ruleb[k].condition[l] == 2:
                        bit_matches += 1

                if bit_matches == rule_length-1:
                    if ruleb[k].output == rulebase[i].output:
                        self.score += 1
                        ruleb[k].matches += 1
                    break

    # This is the mutation function.
    # We allow it to have the opportunity to mutate a wildcard
    # and we make sure it is not in the position of the class

    def mutate(self, gene, rule_l):

        if (gene + 1)  % rule_l == 0:
            if self.chromosome[gene] == 0:
                self.chromosome[gene] = 1
            else :
                self.chromosome[gene] = 0
        else:
            if self.chromosome[gene] == 0:
                self.chromosome[gene] = random.randint(1,2)
            elif self.chromosome[gene] == 1:
                self.chromosome[gene] = random.choice([0,2])
            else:
                self.chromosome[gene] = random.randint(0,1)


if __name__ == "__main__":
    env = gene.Population(Init)

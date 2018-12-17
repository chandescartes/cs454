
from random import randint, shuffle, uniform, sample, uniform
import math

import copy

from lxml import etree

from utils import *

class GA(object):

    def __init__(self, pop_size, eval_lim, mut_rate, mut_k, crossover_rate, tournament_k, use_elitism, use_lin_ranking, dom_filepath, xpath, fitness_values, verbose=True):
        if verbose:
            print("Initializing Genetic Algorithm...")
        self.pop_size = pop_size
        self.eval_lim = eval_lim
        self.crossover_rate = crossover_rate
        self.mut_rate = mut_rate
        self.mut_k = mut_k
        self.use_elitism = use_elitism
        self.use_lin_ranking = use_lin_ranking
        self.tournament_k = tournament_k

        utf8_html_parser = etree.HTMLParser(encoding='utf-8')
        self.DOM = etree.parse(cleanup(dom_filepath),parser=utf8_html_parser)
        elements = self.DOM.xpath(xpath)
        assert len(elements) == 1, "Invalid absolute XPath!"
        self.element = elements[0]
        self.abs_xpath = generate_abs_xpath(self.element)

        self.eval_tot = 0
        self.gen = 1

        self.pop = []
        self.parents = []
        self.children = []
        self.init_pop = []

        self.optimum = None
        self.verbose = verbose

        self.fitness_values = fitness_values

        self.init_population()

        self.printv("Initialization Complete!")

    def printv(self, string):
        if self.verbose:
            print(string)

    def init_population(self):
        self.pop.append(Individual(self, "//*"))
        self.pop.append(Individual(self, self.abs_xpath))
        self.optimum = self.pop[-1]
        levels = parse_xpath(self.abs_xpath)

        for i in range(1, len(levels)):
            indiv = Individual(self, generate_xpath(levels[i:]))
            self.pop.append(indiv)

        if len(self.pop) % 2 != 0:
            self.pop.append(Individual(self, self.abs_xpath))

        self.eval_pop()
        self.pop.sort()
        self.init_pop = self.pop[:]



    def evolve(self):
        # self.optimum = self.pop[0]

        self.printv("  G: {}     \tScore: {} \t{}%".format(self.gen, round(self.optimum.fitness,2), round(self.eval_tot/self.eval_lim*100, 1)))

        while self.eval_tot < self.eval_lim:
            self.select_parents()
            self.create_children()
            self.mutate_children()
            self.form_next_gen()
            self.gen += 1
            if self.optimum > self.pop[0]:
                # print("new opt")
                # print(self.optimum.fitness)
                # print(self.pop[0].fitness)
                self.optimum = copy.deepcopy(self.pop[0])

            if self.gen % 100 == 0:
                self.printv("  G: {0}     \tScore: {1} \tOptimum: {2} \t{3}%".format(self.gen, round(self.pop[0].fitness,2), round(self.optimum.fitness,2) , round(self.eval_tot/self.eval_lim*100, 1)))
                self.save()

            # self.printv("  Evolution Finished")

        self.printv("Score: {} \tXPath: {}".format(self.optimum.xpath, round(self.optimum.fitness, 2)))

    def eval_pop(self):
        for ind in self.pop:
            ind.eval()
            self.eval_tot += 1

    def select_parents(self):
        if self.use_lin_ranking:
            self.parents = []

            n = ((1 + len(self.pop)) * len(self.pop)) / 2
            reverse_ranked = list(reversed(self.pop))

            while len(self.parents) < self.pop_size:
                selector = randint(1, n)
                for i in range(1, len(self.pop) + 1):
                    selector -= i
                    if selector <= 0:
                        break

                parent1 = reverse_ranked[i-1]
                self.parents.append(parent1)

                while True:
                    selector = randint(1, n)
                    for i in range(1, len(self.pop) + 1):
                        selector -= i
                        if selector <= 0:
                            break

                    parent2 = reverse_ranked[i-1]
                    if parent1 is not parent2:
                        self.parents.append(parent2)
                        break

        else:
            self.parents = []
            while len(self.parents) < self.pop_size:
                candidates = sample(self.pop, self.tournament_k)
                self.parents.append(min(candidates))

    def create_children(self):
        self.children = []
        for i in range(0, len(self.parents) // 2):
            parent1 = self.parents[2 * i]
            parent2 = self.parents[2 * i + 1]

            child1, child2 = self.mate(parent1, parent2)

            self.children.append(child1)
            self.children.append(child2)

    def mutate_children(self):
        for child in self.children:
            for k in range(self.mut_k):
                if uniform(0, 1) < self.mut_rate:
                    child.mutate()

    def form_next_gen(self):
        for child in self.children:
            child.eval()
            self.eval_tot += 1

        if self.use_elitism:
            pop = self.pop + self.children
            locators = []
            nonlocators = []
            for ind in pop:
                if ind.get_type():
                    locators.append(ind)
                else:
                    nonlocators.append(ind)

            locators.sort()
            nonlocators.sort()

            self.pop = locators[:math.ceil(len(locators)/2)] + nonlocators[:math.floor(len(nonlocators)/2)]

        else:
            self.pop = self.children
            self.pop.sort()
            if len(self.init_pop) < self.pop_size:
                self.pop = self.pop[:-len(self.init_pop)]
                self.pop = self.pop + self.init_pop
                self.pop.sort()
                
    def mate(self, parent1, parent2):
        if uniform(0, 1) > self.crossover_rate:
            return parent1, parent2
        else:
            len1 = get_xpath_length(parent1.xpath)
            len2 = get_xpath_length(parent2.xpath)

            if len1 <= 1 or len2 <= 1:
                return parent1, parent2
            r = randint(1, min(len1, len2) - 1)
            parsed1 = parse_xpath(parent1.xpath)
            parsed2 = parse_xpath(parent2.xpath)
            child1 = Individual(self, generate_xpath(parsed1[:-r] + parsed2[-r:]))
            child2 = Individual(self, generate_xpath(parsed2[:-r] + parsed1[-r:]))

            return child1, child2

    def save(self):
        # with open('solution.csv', 'w') as csvfile:
        #     writer  = csv.writer(csvfile, delimiter=' ')
        #     for node in self.optimum.path:
        #         writer.writerow([node])
        # TODO
        pass

class Individual(object):

    def __init__(self, ga, xpath):
        self.ga = ga
        self.xpath = xpath
        self.type = self.get_type() # True = pop', False = pop''
        self.fitness_values = self.ga.fitness_values
        self.fitness = self.get_fitness()

        self.transformations = [
            self.trans_add_name,
            self.trans_add_predicate,
            self.trans_add_level,
            self.trans_remove_name,
            self.trans_remove_predicate,
            self.trans_remove_level
        ]

    def __gt__(self, other):
        if self.type == other.type:
            return self.fitness > other.fitness
        return not self.type

    def __lt__(self, other):
        if self.type == other.type:
            return self.fitness < other.fitness
        return self.type

    def __eq__(self, other):
        return self.type == other.type and self.fitness == other.fitness

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    def get_fitness(self):
        self.type = self.get_type()
        if not self.type:
            fitness = len(self.ga.DOM.xpath(self.xpath))
            assert fitness != 0
            return fitness

        fitness = 0
        levels = parse_xpath(self.xpath)
        for level in levels:
            level_dict = level_string_to_dict(level)
            if level_dict['name'] == '*':
                fitness += self.fitness_values[0]
            else:
                fitness += self.fitness_values[1]

            if level_dict['position'] is not None:
                fitness += self.fitness_values[2]

            for attr in level_dict['attributes']:
                if attr.startswith('class'):
                    fitness += self.fitness_values[3]
                elif attr.startswith('id'):
                    fitness += self.fitness_values[4]

        return fitness

    def eval(self):
        self.fitness = self.get_fitness()

    def mutate(self):
        shuffle(self.transformations)
        for option in self.transformations:
            if option():
                break

    def get_type(self):
        elements = self.ga.DOM.xpath(self.xpath)
        if len(elements) != 1:
            return False
        else:
            this, target = elements[0], self.ga.element
            assert this.tag == target.tag and this.tail == target.tail and this.attrib == target.attrib, "Zombie Appeared!"
            return True


    ## Change top level '*' to a tag
    def trans_add_name(self):
        levels = parse_xpath(self.xpath)
        level_dict = level_string_to_dict(levels[0])

        # Cannot add name if top level is not '*'
        if level_dict['name'] != '*':
            return False

        element = get_top_element(self.xpath, self.ga.element)
        level_dict['name'] = element.tag
        if level_dict['position'] is not None:
            level_dict['position'] = get_correct_position(level_dict, element)

        # Update xpath with added name
        levels[0] = level_dict_to_string(level_dict)
        self.xpath = generate_xpath(levels)

        return True

    ## Add predicate (including position) at top level
    def trans_add_predicate(self):
        levels = parse_xpath(self.xpath)
        level_dict = level_string_to_dict(levels[0])
        element = get_top_element(self.xpath, self.ga.element)

        preds = [0] if level_dict['position'] is None else []
        for pred in ["class", "id"]: # FIXME add other attributes?
            if pred in element.keys() and not has_attribute(pred, level_dict):
                preds.append(pred)

        shuffle(preds)

        for pred in preds:
            if pred == 0:
                # Add position predicate
                level_dict['position'] = get_correct_position(level_dict, element)
                levels[0] = level_dict_to_string(level_dict)
                self.xpath = generate_xpath(levels)
                return True
            else:
                # Add named predicate
                level_dict['attributes'].append(pred + "=\"" + element.get(pred) + "\"")
                if level_dict['position'] is not None:
                    level_dict['position'] = get_correct_position(level_dict, element)
                level_string = level_dict_to_string(level_dict)
                levels[0] = level_string
                self.xpath = generate_xpath(levels)
                return True

        return False

    ## Append * to top level
    def trans_add_level(self):
        levels = ['*'] + parse_xpath(self.xpath)

        if get_xpath_length(self.ga.abs_xpath) == get_xpath_length(self.xpath):
            return False

        self.xpath = generate_xpath(levels)
        return True

    ## Change top level tag to '*'
    def trans_remove_name(self):
        levels = parse_xpath(self.xpath)
        level_dict = level_string_to_dict(levels[0])
        element = get_top_element(self.xpath, self.ga.element)

        # Cannot remove name if top level is already '*'
        if level_dict['name'] == '*':
            return True

        level_dict['name'] = '*'
        if level_dict['position'] is not None:
            level_dict['position'] = get_correct_position(level_dict, element)

        levels[0] = level_dict_to_string(level_dict)
        self.xpath = generate_xpath(levels)
        return True

    ## Remove predicate (including position) at top level
    def trans_remove_predicate(self):
        levels = parse_xpath(self.xpath)
        level_dict = level_string_to_dict(levels[0])
        element = get_top_element(self.xpath, self.ga.element)

        preds = level_dict['attributes'][:]
        if level_dict['position'] is not None:
            preds.append(0)

        # Cannot remove predicate if there are none
        if len(preds) == 0:
            return False

        rand = randint(0, len(preds) - 1)
        if preds[rand] == 0:
            level_dict['position'] = None # Remove position
        else:
            del level_dict['attributes'][rand] # Remove named predicate

        if level_dict['position'] is not None:
            level_dict['position'] = get_correct_position(level_dict, element)

        levels[0] = level_dict_to_string(level_dict)
        self.xpath = generate_xpath(levels)

        return True

    ## Remove top level
    def trans_remove_level(self):
        levels = parse_xpath(self.xpath)

        # Cannot remove level if only one level
        if len(levels) <= 1:
            return False

        self.xpath = generate_xpath(levels[1:])
        return True

import random
import csv
from lxml import etree
from collections import defaultdict

from utils import *

class GA(object):

    def __init__(self, pop_size, eval_lim, nodes, mut_rate, dom_filepath, abs_xpath, mut_k=1, use_elitism=False):
        if SHOW_PROGRESS:
            print("Initializing Genetic Algorithm...")
        self.pop_size = pop_size
        self.eval_lim = eval_lim
        self.mut_rate = mut_rate
        self.mut_k = mut_k
        self.use_elitism = use_elitism

        self.DOM = etree.parse(dom_filepath)
        self.abs_xpath = abs_xpath
        self.element = self.DOM.xpath(abs_xpath)

        self.eval_tot = 0
        self.gen = 1

        self.pop = []
        self.parents = []
        self.children = []

        self.optimum = None

        init_population(self)


        if SHOW_PROGRESS:
            print("Initialization Complete!")

    def init_population(self):
        # TODO

    def evolve(self):
        # self.optimum = self.pop[0]
        # if SHOW_PROGRESS:
        #     print("  G: {0}     \tScore: {1} \t{2}%".format(self.gen, round(self.optimum.dist,2), round(self.eval_tot/self.eval_lim*100, 1)))
        # while self.eval_tot < self.eval_lim:
        #     self.select_parents_by_rank()
        #     self.create_children()
        #     self.mutate_children()
        #     self.form_next_gen()
        #     self.gen += 1
        #     self.optimum = self.pop[0]
        #     if SHOW_PROGRESS:
        #         print("  G: {0}     \tScore: {1} \t{2}%".format(self.gen, round(self.optimum.dist,2), round(self.eval_tot/self.eval_lim*100, 1)))
        #     if self.gen % 100 == 0:
        #         self.save()
        # if SHOW_PROGRESS:
        #     print("  Evolution Finished")
        # print(round(self.optimum.dist,2))
        # TODO
        pass

    def eval_pop(self):
        for ind in self.pop:
            ind.eval()
            self.eval_tot += 1
        # TODO
        pass

    def select_parents_by_rank(self):
        # self.parents = []
        # n = ((1 + self.pop_size) * self.pop_size) / 2
        # reverse_ranked = list(reversed(self.pop))
        # while len(self.parents) <  self.pop_size:
        #     selector = random.randint(1, n)
        #     for i in range(1, self.pop_size + 1):
        #         selector -= i
        #         if selector <= 0:
        #             break
        #     parent1 = reverse_ranked[i-1]
        #     self.parents.append(parent1)
        #     while True:
        #         selector = random.randint(1, n)
        #         for i in range(1, self.pop_size + 1):
        #             selector -= i
        #             if selector <= 0:
        #                 break
        #         parent2 = reverse_ranked[i-1]
        #         if parent1 is not parent2:
        #             break
        #     self.parents.append(parent2)
        # TODO
        pass

    def create_children(self):
        # self.children = []
        # for i in range(0, int(self.pop_size / 2)):
        #     parent1 = self.parents[2 * i]
        #     parent2 = self.parents[2 * i + 1]
        #     child1, child2 = self.mate(parent1, parent2)
        #     self.children.append(child1)
        #     self.children.append(child2)
        # TODO
        pass

    def mutate_children(self):
        # for child in self.children:
        #     for k in range(self.mut_k):
        #         rand = random.uniform(0, 1)
        #         if rand < self.mut_rate:
        #             child.mutate()
        # TODO
        pass

    def form_next_gen(self):
        # for child in self.children:
        #     child.eval()
        #     self.eval_tot += 1
        #
        # if self.use_elitism:
        #     pop = self.pop + self.children
        #     pop.sort()
        #     self.pop = pop[:self.pop_size]
        #     while len(pop) > self.pop_size:
        #         del pop[self.pop_size]
        #
        # else:
        #     while len(self.pop) > 0:
        #         del self.pop[0]
        #     self.pop = self.children
        #     self.pop.sort()
        # TODO
        pass

    def mate(self, parent1, parent2):
        # child1 = Individual(self)
        # child2 = Individual(self)
        #
        # while True:
        #     i = random.randint(0, self.dim - 1)
        #     j = random.randint(0, self.dim - 1)
        #     if i == j:
        #         continue
        #     elif i < j:
        #         left = i
        #         right = j
        #         break
        #     else:
        #         left = j
        #         right = i
        #         break
        #
        # for i in range(left, right):
        #     child1.path[i] = parent1.path[i]
        #
        # s = set(parent1.path[left:right])
        # j = 0
        # for i in range(0, self.dim):
        #     if i >= left and i < right:
        #         continue
        #     while parent2.path[j] in s:
        #         j += 1
        #     child1.path[i] = parent2.path[j]
        #     j += 1
        #
        # while True:
        #     i = random.randint(0, self.dim - 1)
        #     j = random.randint(0, self.dim - 1)
        #     if i == j:
        #         continue
        #     elif i < j:
        #         left = i
        #         right = j
        #         break
        #     else:
        #         left = j
        #         right = i
        #         break
        #
        # for i in range(left, right):
        #     child2.path[i] = parent2.path[i]
        #
        # s = set(parent2.path[left:right])
        # j = 0
        # for i in range(0, self.dim):
        #     if i >= left and i < right:
        #         continue
        #     while parent1.path[j] in s:
        #         j += 1
        #     child2.path[i] = parent1.path[j]
        #     j += 1
        #
        # return child1, child2
        # TODO
        pass

    def save(self):
        # with open('solution.csv', 'w') as csvfile:
        #     writer  = csv.writer(csvfile, delimiter=' ')
        #     for node in self.optimum.path:
        #         writer.writerow([node])
        # TODO
        pass

class Individual(object):

    transformations = [
        self.transAddName,
        self.transAddPredicate,
        self.transAddLevel,
        self.transRemoveName,
        self.transRemovePredicate,
        self.transRemoveLevel
    ]

    def __init__(self, ga, xpath):
        self.ga = ga
        self.type = None # True: pop', False: pop'', None: unknown
        self.xpath = xpath


    def eval(self):
        # TODO
        pass

    def mutate(self):
        # TODO
        pass

    def trans_add_name(self):
        abs_xpath = self.ga.abs_xpath
        xpath = self.xpath

        levels = parse_xpath(xpath)

        if levels[0] != '*':
            name = get_top_element(xpath, self.ga.element).tag
            levels[0] = name
            self.xpath = generate_xpath(levels)
            return True
        else:
            return False

    def trans_add_predicate(self):
        abs_xpath = self.ga.abs_xpath
        xpath = self.xpath
        levels = parse_xpath(xpath)
        level_string = levels[0]
        level_dict = level_string_to_dict(level_string)

        element = get_top_element(xpath, self.ga.element):
        keys = element.keys()
        random.shuffle(keys)
        for key in keys:
            if not has_attribute(key, level_dict):
                level_dict['attributes'].append(key+"="+element.get(key))
                level_string = level_dict_to_string(level_dict)
                levels[0] = level_string
                self.xpath = generate_xpath(levels)
                return True
        return False

    def trans_add_level(self):
        abs_xpath = self.ga.abs_xpath
        xpath = self.xpath

        levels = parse_xpath(xpath)
        levels = ['*'] + levels

        self.xpath = generate_xpath(levels):
        return True


    def trans_remove_name(self):
        abs_xpath = self.ga.abs_xpath
        xpath = self.xpath

        levels = parse_xpath(xpath)
        levels[0] = '*'

        self.xpath = generate_xpath(levels)
        return True

    def trans_remove_predicate(self):
        abs_xpath = self.ga.abs_xpath
        xpath = self.xpath

        levels = parse_xpath(xpath)
        level_string = levels[0]
        level_dict = level_string_to_dict(level_string)
        if len(level_dict['attributes']) > 0:
            rand = random.randint(0, len(len(level_dict['attributes'])-1))
            del level_dict['atributes'][rand]
            level_string = level_dict_to_string(level_dict)
            levels[0] = level_string
            self.xpath = generate_xpath(levels):
            return True
        else:
            return False

    def trans_remove_level(self):
        abs_xpath = self.ga.abs_xpath
        xpath = self.xpath

        levels = parse_xpath(xpath)
        if len(levels) > 1:
            levels = levels[1:]
            self.xpath = generate_xpath(levels)
            return True
        else:
            return False


from random import randint, shuffle

from lxml import etree

from utils import *

class GA(object):

    def __init__(self, pop_size, eval_lim, mut_rate, mut_k, use_elitism, dom_filepath, abs_xpath, verbose=True):
        if verbose:
            print("Initializing Genetic Algorithm...")
        self.pop_size = pop_size
        self.eval_lim = eval_lim
        self.mut_rate = mut_rate
        self.mut_k = mut_k
        self.use_elitism = use_elitism

        self.DOM = etree.parse(dom_filepath)
        self.abs_xpath = uniform_quote(abs_xpath)
        elements = self.DOM.xpath(abs_xpath)
        assert len(elements) == 1, "Invalid absolute XPath!"
        self.element = elements[0]
        # for ancestor in self.element.iterancestors():
        #   print(self.DOM.getpath(ancestor))

        self.eval_tot = 0
        self.gen = 1

        self.pop = []
        self.parents = []
        self.children = []

        self.optimum = None
        self.verbose = verbose

        self.init_population()

        if self.verbose:
            print("Initialization Complete!")

    def init_population(self):
        self.pop.append(Individual(self, "//*"))
        self.pop.append(Individual(self, self.abs_xpath))

        levels = parse_xpath(self.abs_xpath)

        for i in range(1, len(levels)):
            indiv = Individual(self, generate_xpath(levels[i:]))
            self.pop.append(indiv)

    def evolve(self):
        # self.optimum = self.pop[0]
        # if self.verbose:
        #     print("  G: {0}     \tScore: {1} \t{2}%".format(self.gen, round(self.optimum.dist,2), round(self.eval_tot/self.eval_lim*100, 1)))
        # while self.eval_tot < self.eval_lim:
        #     self.select_parents_by_rank()
        #     self.create_children()
        #     self.mutate_children()
        #     self.form_next_gen()
        #     self.gen += 1
        #     self.optimum = self.pop[0]
        #     if self.verbose:
        #         print("  G: {0}     \tScore: {1} \t{2}%".format(self.gen, round(self.optimum.dist,2), round(self.eval_tot/self.eval_lim*100, 1)))
        #     if self.gen % 100 == 0:
        #         self.save()
        # if self.verbose:
        #     print("  Evolution Finished")
        # print(round(self.optimum.dist,2))
        # TODO
        for i, ind in enumerate(self.pop):
            print('---------',i+1)
            print(ind.xpath)
            ind.mutate()

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
        len1 = get_xpath_length(parent1.xpath)
        len2 = get_xpath_length(parent2.xpath)

        if len1 <= 1 or len2 <= 1:
            return parent1, parent2

        r1, parsed1 = randint(1, len1 - 1), parse_xpath(parent1.xpath)
        r2, parsed2 = randint(1, len2 - 1), parse_xpath(parent2.xpath)
        child1 = Individual(self, generate_xpath(parsed1[:r1] + parsed2[r2:]))
        child2 = Individual(self, generate_xpath(parsed2[:r2] + parsed1[r1:]))

        # print(parent1.xpath)
        # print(parent2.xpath)
        # print(child1.xpath)
        # print(child2.xpath)

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

        self.transformations = [
            self.trans_add_name,
            self.trans_add_predicate,
            self.trans_add_level,
            self.trans_remove_name,
            self.trans_remove_predicate,
            self.trans_remove_level
        ]


    def eval(self):
        # TODO
        pass

    def mutate(self):
        options = self.transformations[:]
        shuffle(options)
        for option in options:
            if option():
                break
        return


    def get_type(self):
        elements = self.ga.DOM.xpath(self.xpath)
        if len(elements) != 1:
            return False

        this, target = elements[0], self.ga.element
        return this.tag == target.tag \
            and this.tail == target.tail and this.attrib == target.attrib

    def trans_add_name(self):
        xpath = self.xpath
        levels = parse_xpath(xpath)
        level_string = levels[0]
        level_dict = level_string_to_dict(level_string)
        element = get_top_element(xpath, self.ga.element)

        if level_dict['name'] == '*':
            level_dict['name'] = get_top_element(xpath, self.ga.element).tag
            if level_dict['position'] is not None:
                level_dict['position'] = get_correct_position(level_dict, element)
            levels[0] = level_dict_to_string(level_dict)
            self.xpath = generate_xpath(levels)
            return True
        else:
            return False

    def trans_add_predicate(self):
        xpath = self.xpath
        levels = parse_xpath(xpath)
        level_string = levels[0]
        level_dict = level_string_to_dict(level_string)

        element = get_top_element(xpath, self.ga.element)
        keys = element.keys()
        options = [0] + keys
        shuffle(options)
        for option in options:
            if option == 0:
                if level_dict['position'] is None:
                    level_dict['position'] = get_correct_position(level_dict, element)
                    level_string = level_dict_to_string(level_dict)
                    levels[0] = level_string
                    self.xpath = generate_xpath(levels)
                    return True
                else:
                    continue
            else:
                key = option
                if not has_attribute(key, level_dict):
                    level_dict['attributes'].append(key+"=\""+element.get(key)+"\"")
                    if level_dict['position'] is not None:
                        level_dict['position'] = get_correct_position(level_dict, element)
                    level_string = level_dict_to_string(level_dict)
                    levels[0] = level_string
                    self.xpath = generate_xpath(levels)
                    return True
                else:
                    continue
        return False

    def trans_add_level(self):
        abs_xpath = self.ga.abs_xpath
        xpath = self.xpath
        levels = parse_xpath(xpath)
        levels = ['*'] + levels
        if get_xpath_length(abs_xpath) == get_xpath_length(xpath):
            return False
        self.xpath = generate_xpath(levels)
        return True

    def trans_remove_name(self):
        xpath = self.xpath
        levels = parse_xpath(xpath)
        level_string = levels[0]
        level_dict = level_string_to_dict(level_string)
        element = get_top_element(xpath, self.ga.element)

        if level_dict['name'] != '*':
            level_dict['name'] = '*'
            level_dict['position'] = get_correct_position(level_dict, element)
            levels[0] = level_dict_to_string(level_dict)
            self.xpath = generate_xpath(levels)

            return True
        else:
            return False

    def trans_remove_predicate(self):
        xpath = self.xpath
        levels = parse_xpath(xpath)
        level_string = levels[0]
        level_dict = level_string_to_dict(level_string)
        options = level_dict['attributes'][:]
        if level_dict['position'] is not None:
            options.append(0)
        if len(options) > 0:
            rand = randint(0, len(options)-1)
            if options[rand] == 0:
                level_dict['position'] = None
            else:
                del level_dict['atributes'][rand]
            if level_dict['position'] is not None:
                level_dict['position'] = get_correct_position(level_dict, element)
            level_string = level_dict_to_string(level_dict)
            levels[0] = level_string
            self.xpath = generate_xpath(levels)
            return True
        else:
            return False

    def trans_remove_level(self):
        xpath = self.xpath
        levels = parse_xpath(xpath)
        if len(levels) > 1:
            levels = levels[1:]
            self.xpath = generate_xpath(levels)
            return True
        else:
            return False

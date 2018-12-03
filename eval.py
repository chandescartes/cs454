import sys, os
import time
import csv
import argparse
import math

from lxml import etree

from functools import partial
from multiprocessing import Pool


from ga import GA
from utils import *

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", type=int, default=50, help="Set an even number population size (default=50)")
	parser.add_argument("-f", type=int, default=5e+4, help="Set fitness evaluation limit")
	parser.add_argument("-r", type=float, default=0.1, help="Set mutation rate (0.0 ~ 1.0, default=0.1)")
	parser.add_argument("-k", type=int, default=3, help="Set mutation limit per child (default=3)")
	parser.add_argument("-c", type=float, default=0.8, help="Set crossover_rate (0.0 ~ 1.0, default=0.8)")
	parser.add_argument("-t", type=int, default=3, help="Set tournament selection k value(default=3)")
	parser.add_argument("-l", action="store_true", help="Use linear ranking (default=tournament selection)")
	parser.add_argument("-e", action="store_true", help="Use elitism (default=generational_replacement)")
	parser.add_argument("-d", type=str, required=True, help="Specify path to testfile")
	parser.add_argument("-s", action="store_true", help="Show progress")

	return parser.parse_args()



def eval_ga(row, arguments):
	start=time.time()

	args=arguments

	path_old = row[2]
	xpath_old = row[4]
	path_new = row[3]
	xpath_new = row[5]

	fit_val_1=[0.1001, 0.9002, 0.7003, 0.4004, 0.3005]
	fit_val_optimal=fit_val_1 # *, tag, position, class, id

	ga = GA(
		pop_size=args.p,
		eval_lim=args.f,
		mut_rate=args.r,
		mut_k=args.k,
		crossover_rate=args.c,
		tournament_k=args.t,
		use_elitism=args.e,
		use_lin_ranking=args.l,
		dom_filepath=path_old,
		xpath=xpath_old,
		fitness_values=fit_val_optimal,
		verbose=args.s
		)
	ga.select_parents()
	ga.evolve()

	xpath_robust = ga.optimum.xpath
	xpath_fitness = ga.optimum.fitness
	end=time.time()
	# print("{} seconds elapsed.".format(round(end-start,2)))
	return xpath_robust, xpath_fitness


if __name__ == '__main__':
	args = parse_arguments()

	testfile = args.d

	fit_val_2=[0.1, 0.2, 0.7, 0.4, 0.3]


	start = time.time()
	testdata = []

	with open(testfile,"r") as f:
		reader = csv.reader(f)
		line_num = -1
		for row in reader:
			if line_num < 0:
				line_num += 1
				continue
			line_num += 1
			testdata.append(row)

	results = []
	with Pool(len(testdata)) as p:
		results = p.map(partial(eval_ga, arguments=args), testdata)


	end=time.time()
	print("{} seconds elapsed.".format(round(end-start,2)))


	success = 0
	fail = 0
	listfound = 0
	line_num = 0

	for xpath_robust, xpath_fitness in results:
		row=testdata[line_num]
		line_num += 1

		path_new = row[3]
		xpath_new = row[5]

		utf8_html_parser = etree.HTMLParser(encoding='utf-8')
		new_DOM = etree.parse(cleanup(path_new),parser=utf8_html_parser)



		query = new_DOM.xpath(xpath_new)

		assert len(query) == 1, "Multiple items found in new query"
		target = query[0]


		found = new_DOM.xpath(xpath_robust)

		if len(found) != 1:
			print("Test Case {}: Robust xpath failed. Fitness: {}. Elements found: {}".format(line_num, xpath_fitness,len(found)))
			print(xpath_robust)
			print(etree.tostring(target))
			if len(found) > 0:
				print(" ")
				for elem in found:
					print(etree.tostring(elem))
				if (found[0]==target):
					print("List was found.")
					listfound += 1
			fail += 1
			print(" ")
		elif (found[0]==target):
			print("Test Case {}: Found! Fitness: {}".format(line_num, xpath_fitness))
			success += 1

		else:
			print("Test Case {}: Robust xpath is different. Fitness: {}".format(line_num, xpath_fitness))
			fail += 1


		bad_chars = '(){}<> \n\r\t'

	print("{} out of {} cases works.".format(success, success+fail))
	print("{} partials found.".format(listfound))
	# assert this.text.strip(bad_chars) == target.text.strip(bad_chars), "Different elements!"

	end=time.time()
	print("{} seconds elapsed.".format(round(end-start,2)))


def find_weights():
	pass

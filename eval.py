import sys, os
import time
import csv
import argparse

import math
from statistics import mean


from lxml import etree

from functools import partial
from multiprocessing import Pool

from random import *

from ga import GA
from utils import *

from tqdm import tqdm

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", type=int, default=50, help="Set an even number population size (default=50)")
	parser.add_argument("-f", type=int, default=1e+4, help="Set fitness evaluation limit")
	parser.add_argument("-r", type=float, default=0.1, help="Set mutation rate (0.0 ~ 1.0, default=0.1)")
	parser.add_argument("-k", type=int, default=3, help="Set mutation limit per child (default=3)")
	parser.add_argument("-c", type=float, default=0.8, help="Set crossover_rate (0.0 ~ 1.0, default=0.8)")
	parser.add_argument("-t", type=int, default=3, help="Set tournament selection k value(default=3)")
	parser.add_argument("-l", action="store_true", help="Use linear ranking (default=tournament selection)")
	parser.add_argument("-e", action="store_true", help="Use elitism (default=generational_replacement)")
	parser.add_argument("-d", type=str, required=True, help="Specify path to testfile")
	parser.add_argument("-s", action="store_true", help="Show progress")
	parser.add_argument("-P", action="store_true", help="Use parallel computation")

	return parser.parse_args()



def eval_ga(row, arguments, fit_val):
	start=time.time()

	args=arguments

	path_old = row[2]
	xpath_old = row[4]
	path_new = row[3]
	xpath_new = row[5]

	fit_val_temp=fit_val # *, tag, position, class, id
	ga = GA(
		pop_size=args.p,
		eval_lim=args.f,
		mut_rate=args.r,
		mut_k=args.k,
		crossover_rate=args.c,
		tournament_k=args.t,
		use_elitism=args.e,
		use_lin_ranking=args.l,
		dom_filepath=path_old.strip(),
		xpath=xpath_old,
		fitness_values=fit_val_temp,
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

	fit_vals = []
	for i in range(3):
		temp = []
		for j in range(5):
			temp.append(uniform(0,10))
		fit_vals.append(temp)

	param_results = []
	found_list = [False for i in range(len(testdata))]

	testnum = 7

	initialtime = time.time()
	with open("results{}.csv".format(testnum),"w", newline='') as csvfile:
		writer = csv.writer(csvfile)
		for fit_val_set in tqdm(fit_vals,desc='Total'):
			start = time.time()
			result_temp = []
			for i in tqdm(range(5), desc='Current', leave=False):
				results = []
				if args.P:
					with Pool(min(len(testdata),8)) as p:
						results = p.map(partial(eval_ga, arguments=args, fit_val=fit_val_set), testdata)
				else:
					for row in testdata:
						# print(row[2])
						# print(row[4])
						results.append(eval_ga(row, args, fit_val_set))

				time.sleep(1)

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

					final_path = finalize_xpath(xpath_robust)
					found = new_DOM.xpath(xpath_robust)

					if len(found) != 1:
						# print("Test Case {}: Robust xpath failed. Fitness: {}. Elements found: {}".format(line_num, xpath_fitness,len(found)))
						# print(etree.tostring(target))
						if len(found) > 0:
							# print(" ")
							# for elem in found:
							# 	print(etree.tostring(elem))
							for elem in found:
								if elem == target:
									# print("List was found.")
									listfound += 1
									continue
						fail += 1
						# print(" ")
					elif (found[0]==target):
						# print("Test Case {}: Found! Fitness: {}".format(line_num, xpath_fitness))
						success += 1
						found_list[line_num-1] = True
					else:
						# print("Test Case {}: Robust xpath is different. Fitness: {}".format(line_num, xpath_fitness))
						fail += 1
					# print(final_path)
					# bad_chars = '(){}<> \n\r\t'

				# print("{} out of {} cases works.".format(success, success+fail))
				# print("{} partials found.".format(listfound))
				# assert this.text.strip(bad_chars) == target.text.strip(bad_chars), "Different elements!"

				result_temp.append(success+listfound*0.01)

			# print("Params: {} Average: {} Max: {} Min:{}".format(fit_val_set,mean(result_temp),max(result_temp), min(result_temp)))
			result_temp += fit_val_set
			param_results.append(result_temp)
			writer.writerow(result_temp)
			end=time.time()
			# print("{} seconds elapsed.".format(round(end-start,2)))
		end = time.time()
		print("{} seconds elapsed in total.".format(round(end-initialtime)))
	with open("found{}.csv".format(testnum), "w", newline='') as foundfile:
		writer = csv.writer(foundfile)
		writer.writerow(found_list)

def find_weights():
	pass

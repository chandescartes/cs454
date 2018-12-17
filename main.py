import sys, os
import time
import csv
import argparse

from ga import GA

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", type=int, default=50, help="Set an even number population size (default=50)")
	parser.add_argument("-f", type=int, default=1e+4, help="Set fitness evaluation limit")
	parser.add_argument("-r", type=float, default=0.3, help="Set mutation rate (0.0 ~ 1.0, default=0.3)")
	parser.add_argument("-k", type=int, default=3, help="Set mutation limit per child (default=3)")
	parser.add_argument("-c", type=float, default=0.8, help="Set crossover_rate (0.0 ~ 1.0, default=0.8)")
	parser.add_argument("-t", type=int, default=3, help="Set tournament selection k value(default=3)")
	parser.add_argument("-l", action="store_true", help="Use linear ranking (default=tournament selection)")
	parser.add_argument("-e", action="store_true", help="Use elitism (default=generational_replacement)")
	parser.add_argument("-d", type=str, required=True, help="Specify path to testfile")
	parser.add_argument("-s", action="store_true", help="Show progress")

	return parser.parse_args()

if __name__ == '__main__':
	args = parse_arguments()

	xpath = '//article[@class="story theme-main"]/header/div'
	# xpath = '//*[@id="story-header"]/div/div/p/time'


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
	fit_val_1=[5.2, 1.8, 4.8, 8.8, 8.0]
	fit_val_2=[2.1, 9.5, 3.5, 6.1, 7.8]
	fit_val_3=[7.5, 9.1, 4.4, 9.6,-2.1]


	ga = GA(
		pop_size=args.p,
		eval_lim=args.f,
		mut_rate=args.r,
		mut_k=args.k,
		crossover_rate=args.c,
		tournament_k=args.t,
		use_elitism=args.e,
		use_lin_ranking=args.l,
		dom_filepath=args.d,
		xpath=xpath,
		fitness_values=fit_val_optimal,
		verbose=args.s
		)

	ga.select_parents()
	ga.evolve()
	print(fit_val_optimal)

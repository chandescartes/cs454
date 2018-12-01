import sys, os
import time
import csv
import argparse

from ga import GA

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", type=int, default=30, help="Set an even number population size (default=30)")
	parser.add_argument("-f", type=int, default=1e+6, help="Set fitness evaluation limit")
	parser.add_argument("-r", type=float, default=0.1, help="Set mutation rate (0.0 ~ 1.0, default=0.1)")
	parser.add_argument("-k", type=int, default=10, help="Set mutation limit per child (default=10)")
	parser.add_argument("-e", action="store_true", help="Use elitism (default=generational_replacement)")

	parser.add_argument("-d", type=str, required=True, help="Specify path to .html file")
	parser.add_argument("-s", action="store_true", help="Show progress")

	return parser.parse_args()

if __name__ == '__main__':
	args = parse_arguments()
	xpath = "//html[1]/div[@id='div-id']/p[@class='a'][1]"

	for i in range(5):
		fit_val_temp=[10,(i+1),(i+1)/2,(i+1)/3]
		ga = GA(
			pop_size=args.p,
			eval_lim=args.f,
			mut_rate=args.r,
			dom_filepath=args.d,
			xpath=xpath,
			mut_k=args.k,
			use_elitism=args.e,
			fitness_values=fit_val_temp,
			verbose=args.s
			)
		ga.evolve()
		ga.save()
		print(fit_val_temp)




	# ga.pop[0]
    #
    #
	# ind = ga.pop[1]
	# ind.trans_remove_level()
	# print(ind.xpath)
	# ind.trans_remove_level()
	# print(ind.xpath)
	# ind.trans_add_level()
	# print(ind.xpath)
	# ind.trans_add_predicate()
	# print(ind.xpath)
	# ind.trans_add_predicate()
	# print(ind.xpath)

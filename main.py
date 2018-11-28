import sys, os
import time
import csv

import ga

global SHOW_PROGRESS
pop_size = 30
eval_lim = 1e+6
mut_rate = 0.1
mut_k = 10
use_elitism = False

GUIDE = '\nUsage:\n\tpython main.py [options]\n\nOptions:\n\t-p\tSet an even number population size (default=30)\n\t-f\tSet fitness evaluation limit\n\t-r\tSet mutation rate (0.0 ~ 1.0, default=0.1)\n\t-k\tSet mutation limit per child (default=10)\n\t-s\tShow progress\n\t-m\tUse MST approximation\n\t-e\tUse elitism (default=generational_replacement)\n'

ga = GA(pop_size, eval_lim, nodes, mut_rate, dom_filepath, use_elitism=use_elitism)
ga.evolve()
ga.save()

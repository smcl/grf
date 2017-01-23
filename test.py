#!/usr/bin/python

import random
from pprint import pprint
from grf import (
    ClassifiedObject,
    DecisionTreeGenerator,
    DecisionTreeEnv,
    Mutator
)

class Iris(ClassifiedObject):
    def __init__(self, sepal_length, sepal_width, petal_length, petal_width):
        self.sepal_length = float(sepal_length)
        self.sepal_width = float(sepal_width)
        self.petal_length = float(petal_length)
        self.petal_width = float(petal_width)

def parse_data(filename):
    data = []
    f = open(filename)
    lines = f.readlines()
    f.close()

    for line in lines:
        if line:
            (sepal_length, sepal_width, petal_length, petal_width, classification) = line.strip().split(",")
            data.append((Iris(sepal_length, sepal_width, petal_length, petal_width), classification))
    return data

iris_data = parse_data("./iris.data")

#---------------------------------------
# usage - need to abstract fitness into own class

env = DecisionTreeEnv(iris_data)

dtg = DecisionTreeGenerator(env)

from copy import deepcopy

num_trees = 40
num_generations = 1000

mut = Mutator(env)


dt_population = [ dtg.generate() for i in range(num_trees) ]
test_data = random.sample(iris_data, 100) # should be something like random.sample(test_data, 100)
cull_threshold = int(len(dt_population) * 0.25)

def calc_fitness(dt):
    dt.fitness = 0
    for test in test_data:
        input_val = test[0]
        expected = test[1]
        actual = dt.classify(input_val)
        if actual == expected:
            dt.fitness += 1

def print_stats(dt_pop, recalc):
    if recalc:
        dt_pop.sort(key = lambda dt: dt.fitness)
    fitnesses = [ dt.fitness for dt in dt_pop ]

    print("avg_fitness = %d" % (sum(fitnesses) / float(len(dt_pop))))
    print("best_fitness = %d" % (max(fitnesses)))
    print("worst_fitness = %d" % (min(fitnesses)))

for i in range(num_generations):
    print i
    #print len(dt_population)
    for dt in dt_population:
        dt_mut = deepcopy(dt)
        mut.mutate(dt_mut)
        calc_fitness(dt)
        calc_fitness(dt_mut)
        if dt_mut.fitness > dt.fitness:
            dt = dt_mut
    dt_population.sort(key = lambda dt: dt.fitness, reverse = True)
    #print(dt_population[-1].fitness)
    print_stats(dt_population, False)

    useless_count = len([ x for x in dt_population if not x.fitness ])
    to_cull = max(cull_threshold, useless_count)
    print "culling %d" % (to_cull)
    print "len(dt_population) = %d" % (len(dt_population))

    del dt_population[-to_cull:]
    dt_population += [ dtg.generate() for i in range(to_cull) ]

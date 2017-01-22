#!/usr/bin/python

from pprint import pprint
from grf import (
    ClassifiedObject,
    DecisionTreeGenerator
)

class Iris(ClassifiedObject):
    def __init__(self, sepal_length, sepal_width, petal_length, petal_width):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width

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

training_data = parse_data("./iris.data")

#---------------------------------------
# usage

dtg = DecisionTreeGenerator(training_data)


trees = [ dtg.generate() for i in range(100) ]
dt = dtg.generate()


t = training_data[0][0]
c = dt.Classify(t)

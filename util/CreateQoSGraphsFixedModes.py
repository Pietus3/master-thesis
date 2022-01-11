import os
import pickle
from typing import Counter
import numpy as np
import random
import matplotlib.pyplot as plt

dir_path = ''

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/5Modes/evaluationILP0.data', "rb") as fp:   # Unpickling
    evalutationILP5 = pickle.load(fp)

with open('C:/Users/Jan/Desktop/AlgoRecreated//simdata/FixedModes/5Modes/evaluationGreedy0.data', "rb") as fp:   # Unpickling
    evalutationGreedy5 = pickle.load(fp)



sumGreedy = 0
sumILP = 0

counter = 0

indexMode = 3

valuesILP = dict()
valuesGreedy = dict()


for elem1,elem2,elem3,elem4,elem5 in evalutationILP5:
    if elem5 == 1:
        if elem3 in valuesILP:
            valuesILP[elem3].append(elem1)
        else:
            valuesILP[elem3] = [elem1]

for elem1,elem2,elem3,elem4,elem5 in evalutationGreedy5:
    if elem5 == 1:
        if elem3 in valuesGreedy:
            
            valuesGreedy[elem3].append(elem1)
        else:
            valuesGreedy[elem3] = [elem1]

toPlot = []



for itemx,itemy in valuesILP.items():
    if itemx in valuesGreedy:
        if len(valuesGreedy[itemx]) >10:
            sumGreedy = sum(valuesGreedy[itemx])
            lenGreedy = len(valuesGreedy[itemx])
            avGreedy = sumGreedy / lenGreedy 
            avILP = sum(valuesILP[itemx]) / len(valuesILP[itemx])
            value = avGreedy / avILP
            toPlot.append((itemx,value))
    else:
        print("FEHLER")

plt.xlabel('Count total Tasks')
plt.ylabel('avgQoSGreedy / avgQoSILP')

plt.scatter(*zip(*toPlot))

plt.show()
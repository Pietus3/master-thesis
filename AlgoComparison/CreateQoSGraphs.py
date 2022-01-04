import os
import pickle
from typing import Counter
import numpy as np
import random
import matplotlib.pyplot as plt

dir_path = ''

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/10Modes/evaluationILP0.data', "rb") as fp:   # Unpickling
    evalutationILP5 = pickle.load(fp)

with open('C:/Users/Jan/Desktop/AlgoRecreated//simdata/FixedModes/10Modes/evaluationGreedy0.data', "rb") as fp:   # Unpickling
    evalutationGreedy5 = pickle.load(fp)

QoSDataGreedy = dict()
QoSDataILP = dict()

sumGreedy = 0
sumILP = 0

counter = 0



for i in range (0,len(evalutationILP5)):
    if evalutationGreedy5[i][4] == 1:
        QoSDataGreedy[counter] = evalutationGreedy5[i][0]
        QoSDataILP[counter]= evalutationILP5[i][0]

        sumILP = sumILP + evalutationILP5[i][0]
        sumGreedy = sumGreedy + evalutationGreedy5[i][0]
        counter = counter + 1

valuesILP =[]
valuesGreedy = []


labels = [i for i in range(1,11)]

ids = [random.randint(0,len(QoSDataILP)) for i in range(1,11)]

for id in ids:
    valuesILP.append(QoSDataILP[id])
    valuesGreedy.append(QoSDataGreedy[id])

labels.append("average")

valuesGreedy.append(sumGreedy/len(QoSDataGreedy))
valuesILP.append(sumILP/len(QoSDataILP))

print(len(QoSDataILP))
print(len(QoSDataGreedy))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, valuesILP, width, label='ILP')
rects2 = ax.bar(x + width/2, valuesGreedy, width, label='Greedy')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('QoS Value')
ax.set_xlabel('ID')
ax.set_title('QoS Values by ILP and Greedy approach')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()
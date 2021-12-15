import pickle

import time
import matplotlib.pyplot as plt 
from math import log

STATIC_VARIABLEUTILAZATION = 6
STATIC_VARIABLEQOS = 3
STATIC_VARIABLEID = 5


with open("readme.txt", "rb") as fp:   # Unpickling
    taskSets = pickle.load(fp)

# Prepare Data


evaluation = []

for taskSet in taskSets:
    for task in taskSet:
        task.sort(key=lambda x: x[STATIC_VARIABLEUTILAZATION],reverse = True)


    for task in taskSet:
        print(task)

    timingStart = time.perf_counter_ns()

    while sum(number[0][STATIC_VARIABLEUTILAZATION] for number in taskSet) >1:
        biggestCriteria = -1
        biggestCriteriaIndex = -1
        index = 0
        for task in taskSet:
            if len(task)>1 and task[0][STATIC_VARIABLEUTILAZATION] > biggestCriteria:
                biggestCriteria = task[0][STATIC_VARIABLEUTILAZATION]
                biggestCriteriaIndex =index
            index = index + 1

        if biggestCriteriaIndex != -1:
            del taskSet[biggestCriteriaIndex][0]     
        else:
            break


    for task in taskSet:
        task.sort(key=lambda x: x[STATIC_VARIABLEQOS],reverse = True)

    elapsed_time = time.perf_counter_ns() - timingStart

    countTask = len(taskSet)

    countMode = sum([len(task) for task in taskSet])

    sumQoS = sum([task[0][STATIC_VARIABLEQOS] for task in taskSet])

    evaluation.append((sumQoS,elapsed_time/1000,countTask,countMode))

    for task in taskSet:
        print(task[0][STATIC_VARIABLEID])

testList2 = [(elem4, elem2) for elem1, elem2, elem3, elem4 in evaluation]

testList3 = [(elem4, elem1) for elem1, elem2, elem3, elem4 in evaluation]

plt.title("Anzahl Modes x | elapsed Time(Mikrosekunde) y")

plt.scatter(*zip(*testList2))
plt.show()

plt.title("Anzahl Modes x | QoS y")
plt.scatter(*zip(*testList3))
plt.show()
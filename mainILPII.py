import pickle
import time
import matplotlib.pyplot as plt 
from math import log

import numpy

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from pulp import PULP_CBC_CMD

STATIC_VARIABLEQOS = 3

STATIC_VARIABLEPRIO = 4

STATIC_VARIABLEID = 5

STATIC_VARIABLEUTILAZATION = 6

with open("testSets.test", "rb") as fp:   # Unpickling
    taskSets = pickle.load(fp)

evaluation = []

for taskSet in taskSets:
    print("START TASKSET")

    timingStart = time.perf_counter_ns()

    model = LpProblem(name="small-problem", sense=LpMaximize)

    xVariable = dict()
    weightsX= dict()

    i = 0
    for task in taskSet:
        print(task)
        print(i)
        i = i+1

        yVariable = dict()
        weightsY= dict()
        for m in task:
            print("mode: " + str(m))
            nameVar = m[5].split("|")
            point = LpVariable(name=m[5],lowBound = 0,cat="Binary")
            yVariable[nameVar[1]] = point
            print("YVARIABLE " + str(yVariable))
            weightsY[nameVar[1]] = m[STATIC_VARIABLEQOS]# finde Value Stell
        xVariable[nameVar[0]] = yVariable
        print("Inter"+ str(xVariable))
        weightsX[nameVar[0]] = weightsY

    print(xVariable)
    print(weightsX)


    print(xVariable)
    for s in taskSet:
        for v in s:
            print(v)
            print(xVariable[v[5].split("|")[0]][v[5].split("|")[1]])
    
    
    #model+= lpSum(lpSum([xVariable[v[5].split("|")[0]][v[5].split("|")[1]]*weightsX[v[5].split("|")[0]][v[5].split("|")[1]] for v in s] for s in taskSet))

    print(model)

    i = 0

    for t in taskSet:
        model += lpSum(xVariable[i][k] for k in range(0,len(t)))==1
        i = i+1


    modesVisit = []
    modesVariable = []

    for task in taskSet:
       # print(task)
        for mode in task:
        #    print("mode" + str(mode))
            coord = mode[STATIC_VARIABLEID].split("t") 
            modesVariable.append(coord)
            modesVisit.append(mode)

        #    print("xVariable" + str(xVariable))
        #    print("modesVariable: " + str(modesVariable))

            m = numpy.array(xVariable)
        #    print(m.shape)

            model += lpSum(xVariable[int(modesVariable[0][0])][int(modesVariable[0][1])] * modesVisit[i][STATIC_VARIABLEUTILAZATION] for i in range(0,len(modesVisit))) <=1



    status  =model.solve(PULP_CBC_CMD(msg=False))

    print(f"status: {model.status}, {LpStatus[model.status]}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")

    elapsed_time = time.perf_counter_ns() - timingStart

    countTask = len(taskSet)

    countMode = sum([len(task) for task in taskSet])

    evaluation.append((model.objective.value(),elapsed_time/1000,countTask,countMode,status))

testList2 =[]
testList3 = []

for elem1, elem2, elem3, elem4, elem5 in evaluation:
    if elem5 == 1:
        testList2.append((elem4, elem2)) 
        testList3.append((elem4, elem1))


#plt.scatter(*zip(*testList2))
#plt.show()

#plt.scatter(*zip(*testList3))
#plt.show()
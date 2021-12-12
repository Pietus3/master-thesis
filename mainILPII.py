import pickle
import time
import matplotlib.pyplot as plt 
from math import log

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

STATIC_VARIABLEQOS = 3

STATIC_VARIABLEPRIO = 4

STATIC_VARIABLEID = 5

STATIC_VARIABLEUTILAZATION = 6

with open("readme.txt", "rb") as fp:   # Unpickling
    taskSets = pickle.load(fp)


evaluation = []

for taskSet in taskSets:
    timingStart = time.perf_counter_ns()

    model = LpProblem(name="small-problem", sense=LpMaximize)

    xVariable = []
    weightsX=[]

    values = dict()

    i=0

    for task in taskSet:
        k=0
        yVariable = []
        weightsY=[]
        for m in task:
            nameVar = str(i)+"t"+str(k) 
            point = LpVariable(name=nameVar,lowBound = 0,cat="Binary")
            yVariable.append(point)
            values[m[5]] = nameVar
            weightsY.append(m[STATIC_VARIABLEQOS])# finde Value Stell
            k = k+1
        xVariable.append(yVariable)
        weightsX.append(weightsY)
        i=i+1

    model+= lpSum(lpSum([xVariable[s][v]*weightsX[s][v] for v in range(0,len(xVariable[s]))] for s in range(0,len(xVariable))))

    i = 0

    for t in taskSet:
        model += lpSum(xVariable[i][k] for k in range(0,len(t)))==1
        i = i+1

    listOfALLModes = []

    for task in taskSet:
        for k in task:
            listOfALLModes.append(k)

    listOfALLModes.sort(key=lambda x: x[STATIC_VARIABLEPRIO],reverse = True)


    modesVisit = []
    modesVariable = []

    for t in listOfALLModes:
        #p = values[t]
        coord = t[STATIC_VARIABLEID].split("t")
        modesVariable.append(coord)
        modesVisit.append(t)

        model += lpSum([xVariable[int(modesVariable[i][0])][int(modesVariable[i][1])] * modesVisit[i][STATIC_VARIABLEUTILAZATION] for i in range(0,len(modesVisit))]) <=1


    status  =model.solve()

    elapsed_time = time.perf_counter_ns() - timingStart

    evaluation.append((model.objective.value(),elapsed_time))

#print(evaluation)
testList2 = [(elem1, elem2) for elem1, elem2 in evaluation]

print(testList2)

plt.scatter(*zip(*testList2))
plt.show()
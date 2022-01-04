from re import I

from pulp.utilities import value
from CreateTestdata import TestDataCreater
from TaskClasses import TaskSet
from Solver import ILP,Greedy
import matplotlib.pyplot as plt
from pathlib import Path
import pickle
import os


creater = TestDataCreater()

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + '/simdata/FixedModes/5Modes/run0.data', "rb") as fp:   # Unpickling
    dataSets = pickle.load(fp)


evalutationILP = []
evalutationGreedy = []

for data in dataSets:
    
    solverILP = ILP(data.taskList)
    (item1,item2) = solverILP.generate()
    evalutationILP.append(item2)
    solverGreedy = Greedy(data.taskList)
    (item1,item2) = solverGreedy.generate()
    evalutationGreedy.append(item2)

with open(dir_path + '/simdata/evaluationILP0.data', 'wb') as f:
    pickle.dump(evalutationILP,f)

with open(dir_path + '/simdata/evaluationGreedy0.data', 'wb') as f:
    pickle.dump(evalutationGreedy,f)




dataListILPTime =[]
dataListILPQOS = []
dataListGreedyTime =[]
dataListGreedyQOS = []

for elem1, elem2, elem3, elem4, elem5 in evalutationILP:
    if elem5 == 1:
        dataListILPTime.append((elem4, elem2)) 
        dataListILPQOS.append((elem4, elem1))

for elem1, elem2, elem3, elem4, elem5 in evalutationGreedy:
    if elem5 == 1:
        dataListGreedyTime.append((elem4, elem2)) 
        dataListGreedyQOS.append((elem4, elem1))


averageResponseTimeILP = dict()
averageResponseTimeGreedy = dict()

for datax,datay in dataListILPTime:
    if datax in averageResponseTimeILP:
        averageResponseTimeILP[datax].append(datay)
    else:
        averageResponseTimeILP[datax] = [datay]

for datax,datay in dataListGreedyTime:
    if datax in averageResponseTimeGreedy:
        averageResponseTimeGreedy[datax].append(datay)
    else:
        averageResponseTimeGreedy[datax] = [datay]

plotListILPTime = []
plotListGreedyTime = []

for itemx,itemy in averageResponseTimeILP.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeILP[itemx]) >5:
        plotListILPTime.append((itemx,averageValue))

for itemx,itemy in averageResponseTimeGreedy.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeGreedy[itemx]) >5:
        plotListGreedyTime.append((itemx,averageValue))


plt.scatter(*zip(*plotListILPTime))
plt.show()

plt.scatter(*zip(*plotListGreedyTime))
plt.show()

plotListQoSAnalyis = []

dictQoSAnalysis = dict()

if len(dataListILPQOS) == len(dataListGreedyQOS):
    for i in range(len(dataListGreedyQOS)):
        if dataListILPQOS[i][1] in dictQoSAnalysis:
            dictQoSAnalysis[dataListILPQOS[i][1]].append(dataListILPQOS[i][1]-dataListGreedyQOS[i][1])
        else:
            dictQoSAnalysis[dataListILPQOS[i][1]] = [dataListILPQOS[i][1]-dataListGreedyQOS[i][1]]

#print(dictQoSAnalysis)

for elem in dictQoSAnalysis:
    value = sum(dictQoSAnalysis[elem])/len(dictQoSAnalysis[elem])
    plotListQoSAnalyis.append((elem,value))

#print(plotListQoSAnalyis)

plt.scatter(*zip(*plotListQoSAnalyis))

plt.show()
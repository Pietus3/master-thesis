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

dataSets = creater.createTaskSetFixedModesCount(40,200,5,15,0.2,10)

dir_path = os.path.dirname(os.path.realpath(__file__))
Path(dir_path+ "/simdata").mkdir(parents=True, exist_ok=True)

i = 0

while os.path.exists(dir_path + "/simdata/run%s.data" % i):
    i += 1


with open(dir_path + '/simdata/run'+ str(i)+'.data', 'wb') as f:
    pickle.dump(dataSets,f)

with open(dir_path + '/simdata/run'+ str(i)+'.txt', 'w') as f:
    output = []
    for data in dataSets:
        output.append(data.printTaskSetFormat())
    f.write(str(output))


evalutationILP = []
evalutationGreedy = []

for data in dataSets:
    
    solverILP = ILP(data.taskList)
    (item1,item2) = solverILP.generate()
    evalutationILP.append(item2)
    solverGreedy = Greedy(data.taskList)
    (item1,item2) = solverGreedy.generate()
    evalutationGreedy.append(item2)

with open(dir_path + '/simdata/evaluationILP'+ str(i)+'.data', 'wb') as f:
    pickle.dump(evalutationILP,f)

with open(dir_path + '/simdata/evaluationGreedy'+ str(i)+'.data', 'wb') as f:
    pickle.dump(evalutationGreedy,f)




dataListILPTime =[]
dataListILPQOS = []
dataListGreedyTime =[]
dataListGreedyQOS = []

for elem1, elem2, elem3, elem4, elem5 in evalutationILP:
    if elem5 == 1:
        dataListILPTime.append((elem3, elem2)) 
        dataListILPQOS.append((elem3, elem1))

for elem1, elem2, elem3, elem4, elem5 in evalutationGreedy:
    if elem5 == 1:
        dataListGreedyTime.append((elem3, elem2)) 
        dataListGreedyQOS.append((elem3, elem1))


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
    print(len(itemy))
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeILP[itemx]) >5:
        plotListILPTime.append((itemx,averageValue))

for itemx,itemy in averageResponseTimeGreedy.items():
    print(len(itemy))
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeGreedy[itemx]) >5:
        plotListGreedyTime.append((itemx,averageValue))


plt.scatter(*zip(*plotListILPTime))
plt.show()

plt.scatter(*zip(*plotListGreedyTime))
plt.show()

#plotListQoSAnalyis = []

#dictQoSAnalysis = dict()

#if len(dataListILPQOS) == len(dataListGreedyQOS):
#    for i in range(len(dataListGreedyQOS)):
#        if dataListILPQOS[i][1] in dictQoSAnalysis:
#            dictQoSAnalysis[dataListILPQOS[i][1]].append(dataListILPQOS[i][1]-dataListGreedyQOS[i][1])
#        else:
#            dictQoSAnalysis[dataListILPQOS[i][1]] = [dataListILPQOS[i][1]-dataListGreedyQOS[i][1]]

#print(dictQoSAnalysis)

#for elem in dictQoSAnalysis:
#    value = sum(dictQoSAnalysis[elem])/len(dictQoSAnalysis[elem])
#    plotListQoSAnalyis.append((elem,value))

#print(plotListQoSAnalyis)

#plt.scatter(*zip(*plotListQoSAnalyis))

#plt.show()
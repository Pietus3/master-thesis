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

#Creating Testset, also possible to load old Data in Script (need changes)
dataSets = creater.createTaskSetFixedModesCount(40,5,5,15,0.2,10)

dir_path = os.path.dirname(os.path.realpath(__file__))
Path(dir_path+ "/simdata").mkdir(parents=True, exist_ok=True)

i = 0

while os.path.exists(dir_path + "/simdata/run%s.data" % i):
    i += 1


#Safe Testdata to execute experiment again
with open(dir_path + '/simdata/run'+ str(i)+'.data', 'wb') as f:
    pickle.dump(dataSets,f)

with open(dir_path + '/simdata/run'+ str(i)+'.txt', 'w') as f:
    output = []
    for data in dataSets:
        output.append(data.printTaskSetFormat())
    f.write(str(output))


evalutationILP = []
evalutationGreedy = []

#Execute for every testset the different Algorithms
for data in dataSets:
    solverILP = ILP(data.taskList)
    (item1,item2) = solverILP.generate()
    evalutationILP.append(item2)
    solverGreedy = Greedy(data.taskList)
    (item1,item2) = solverGreedy.generate()
    evalutationGreedy.append(item2)

#safe Data to analyse

with open(dir_path + '/simdata/evaluationILP'+ str(i)+'.data', 'wb') as f:
    pickle.dump(evalutationILP,f)

with open(dir_path + '/simdata/evaluationGreedy'+ str(i)+'.data', 'wb') as f:
    pickle.dump(evalutationGreedy,f)




dataListILPTime =[]

dataListGreedyTime =[]


for elem1, elem2, elem3, elem4, elem5 in evalutationILP:
    if elem5 == 1:
        dataListILPTime.append((elem3, elem2)) 

for elem1, elem2, elem3, elem4, elem5 in evalutationGreedy:
    if elem5 == 1:
        dataListGreedyTime.append((elem3, elem2)) 


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
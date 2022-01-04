import pickle
import os
import matplotlib.pyplot as plt
import random
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/5Modes/evaluationILP0.data', "rb") as fp:   # Unpickling
    evalutationILP5 = pickle.load(fp)

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/5Modes/evaluationGreedy0.data', "rb") as fp:   # Unpickling
    evalutationGreedy5 = pickle.load(fp)

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/7Modes/evaluationILP0.data', "rb") as fp:   # Unpickling
    evalutationILP7 = pickle.load(fp)

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/7Modes/evaluationGreedy0.data', "rb") as fp:   # Unpickling
    evalutationGreedy7 = pickle.load(fp)

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/10Modes/evaluationILP0.data', "rb") as fp:   # Unpickling
    evalutationILP10 = pickle.load(fp)

with open('C:/Users/Jan/Desktop/AlgoRecreated/simdata/FixedModes/10Modes/evaluationGreedy0.data', "rb") as fp:   # Unpickling
    evalutationGreedy10 = pickle.load(fp)

dataListILPTime5 =[]
dataListILPQOS5 = []
dataListGreedyTime5 =[]
dataListGreedyQOS5 = []

dataListILPTime7 =[]
dataListILPQOS7 = []
dataListGreedyTime7 =[]
dataListGreedyQOS7 = []

dataListILPTime10 =[]
dataListILPQOS10 = []
dataListGreedyTime10 =[]
dataListGreedyQOS10 = []

counter=0



for elem1, elem2, elem3, elem4, elem5 in evalutationILP5:
    #if elem5 == 1:
        dataListILPTime5.append((elem3, elem2,counter)) 
        dataListILPQOS5.append((elem4, elem1,counter))
        counter=counter+1

counter=0
for elem1, elem2, elem3, elem4, elem5 in evalutationGreedy5:
    #if elem5 == 1:
        dataListGreedyTime5.append((elem3, elem2,counter)) 
        dataListGreedyQOS5.append((elem4, elem1,counter))
        counter=counter+1


for elem1, elem2, elem3, elem4, elem5 in evalutationILP7:
    #if elem5 == 1:
        dataListILPTime7.append((elem3, elem2)) 
        dataListILPQOS7.append((elem3, elem1))

for elem1, elem2, elem3, elem4, elem5 in evalutationGreedy7:
    #if elem5 == 1:
        dataListGreedyTime7.append((elem3, elem2)) 
        dataListGreedyQOS7.append((elem3, elem1))

for elem1, elem2, elem3, elem4, elem5 in evalutationILP10:
    #if elem5 == 1:
        dataListILPTime10.append((elem3, elem2)) 
        dataListILPQOS10.append((elem3, elem1))

for elem1, elem2, elem3, elem4, elem5 in evalutationGreedy10:
    #if elem5 == 1:
        dataListGreedyTime10.append((elem3, elem2)) 
        dataListGreedyQOS10.append((elem3, elem1))


averageResponseTimeILP5 = dict()
averageResponseTimeGreedy5 = dict()
averageResponseTimeILP7 = dict()
averageResponseTimeGreedy7 = dict()
averageResponseTimeILP10 = dict()
averageResponseTimeGreedy10 = dict()

for datax,datay,counter in dataListILPTime5:
    if datax in averageResponseTimeILP5:
        averageResponseTimeILP5[datax].append(datay)
    else:
        averageResponseTimeILP5[datax] = [datay]

for datax,datay,counter in dataListGreedyTime5:
    if datax in averageResponseTimeGreedy5:
        averageResponseTimeGreedy5[datax].append(datay)
    else:
        averageResponseTimeGreedy5[datax] = [datay]

for datax,datay in dataListILPTime7:
    if datax in averageResponseTimeILP7:
        averageResponseTimeILP7[datax].append(datay)
    else:
        averageResponseTimeILP7[datax] = [datay]

for datax,datay in dataListGreedyTime7:
    if datax in averageResponseTimeGreedy7:
        averageResponseTimeGreedy7[datax].append(datay)
    else:
        averageResponseTimeGreedy7[datax] = [datay]

for datax,datay in dataListILPTime10:
    if datax in averageResponseTimeILP10:
        averageResponseTimeILP10[datax].append(datay)
    else:
        averageResponseTimeILP10[datax] = [datay]

for datax,datay in dataListGreedyTime10:
    if datax in averageResponseTimeGreedy10:
        averageResponseTimeGreedy10[datax].append(datay)
    else:
        averageResponseTimeGreedy10[datax] = [datay]


plotListILPTime5 = []
plotListGreedyTime5 = []

plotListILPTime7 = []
plotListGreedyTime7 = []
plotListILPTime10 = []
plotListGreedyTime10 = []

minData = 5

for itemx,itemy in averageResponseTimeILP5.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeILP5[itemx]) >minData:
        plotListILPTime5.append((itemx,averageValue))

for itemx,itemy in averageResponseTimeGreedy5.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeGreedy5[itemx]) >minData:
        plotListGreedyTime5.append((itemx,averageValue))


for itemx,itemy in averageResponseTimeILP7.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeILP7[itemx]) >minData:
        plotListILPTime7.append((itemx,averageValue))

for itemx,itemy in averageResponseTimeGreedy7.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeGreedy7[itemx]) >minData:
        plotListGreedyTime7.append((itemx,averageValue))


for itemx,itemy in averageResponseTimeILP10.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeILP10[itemx]) >minData:
        plotListILPTime10.append((itemx,averageValue))

for itemx,itemy in averageResponseTimeGreedy10.items():
    averageValue = sum(itemy)/len(itemy)
    if len(averageResponseTimeGreedy10[itemx]) >minData:
        plotListGreedyTime10.append((itemx,averageValue))


plt.scatter(*zip(*plotListILPTime5),label = "ILP 5 Modes")
plt.scatter(*zip(*plotListILPTime7),label = "ILP 7 Modes")
plt.scatter(*zip(*plotListILPTime10),label = "ILP 10 Modes")

plt.xlabel('Count total Tasks')
# Set the y axis label of the current axis.
plt.ylabel('run time in ms')
# Set a title of the current axes.
plt.title('Executiontime ILP Fixed Modes')

plt.legend()
plt.show()

plt.scatter(*zip(*plotListGreedyTime5),label = "Greedy 5 Modes")
plt.scatter(*zip(*plotListGreedyTime7),label = "Greedy 7 Modes")
plt.scatter(*zip(*plotListGreedyTime10),label = "Greedy 10 Modes")

plt.xlabel('Count total Modes')
# Set the y axis label of the current axis.
plt.ylabel('run time in ms')
# Set a title of the current axes.
plt.title('Executiontime Greedy Fixed Tasks')

plt.legend()
plt.show()



labels = [i for i in range(1,11)]

ids = [random.randint(0,len(dataListILPQOS5)) for i in range(1,11)]

valuesGreedy = []
valuesILP = []

for id in ids:
    valuesILP.append((dataListILPQOS5[id][1],dataListILPQOS5[id][2]))
    valuesGreedy.append((dataListGreedyQOS5[id][1],dataListGreedyQOS5[id][2]))

print(valuesILP)
print(valuesGreedy)


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, valuesILP, width, label='ILP')
rects2 = ax.bar(x + width/2, valuesGreedy, width, label='Greedy')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()
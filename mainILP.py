import random
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import time

class Mode:
    
    def __init__(self,id,c, t, d, q, p):
        self.comp = c
        self.interArrival = t
        self.relDeadline = d
        self.q = q
        self.p = p
        self.id = id

    def printParameters(self):
        print("MODEID: " + str(self.id) + " \n Die WCET beträgt: "+ str(self.comp) + ", die inter-arrival Time beträgt: "
        + str(self.interArrival)+ ". die relative Deadline Beträgt: " + str(self.relDeadline) +". Der QoS-Value beträgt: " + str(self.q)+". Die Priorität des Modes liegt bei: "+ str(self.p))

class Task:
    def __init__(self, id, modes):
        self.id = id
        self.modeList = []

        for mode in modes:
            self.modeList.append(mode)
    
    def printTask(self):
        print("TASKID" + str(self.id))
        for mode in self.modeList:
            mode.printParameters()

    def checkConstrainedDeadlines(self):
        for mode in self.modeList:
            if not mode.relDeadline <= mode.interArrival:
                return False 
        return True

    def checkImplicitDeadlines(self):
        for mode in self.modeList:
            if not mode.relDeadline == mode.interArrival:
                return False 
        return True


class TaskSet:
    def __init__(self,tasks):
        self.taskList = []
        for task in tasks:
            self.taskList.append(task)

    def addTask(self, task):
        self.taskList.append(task)

    def printTasks(self):
        for task in self.taskList:
            task.printTask()


def createTestdata(intTasks,intModes, intQoS, floatWCET, maxPrio):
    tasks = []
    for k in range(0,random.randint(1,intTasks)):
        modes = []
        ranModes = random.randint(1,intModes)

        for i in range(0,ranModes):
            relDeadline =random.uniform(0,1)
            mode= Mode(i,round(random.uniform(0,floatWCET),3),round(relDeadline,3),round(relDeadline,3),random.randint(0,intQoS),random.randint(0,maxPrio))
            modes.append(mode)
        
        tasks.append(Task(k,modes))
    
    return TaskSet(tasks)


testdata = createTestdata(5,5,15,0.1,7)


testdata.printTasks()


timingStart = time.perf_counter_ns()

print(timingStart)


model = LpProblem(name="small-problem", sense=LpMaximize)

x = []
weightsX=[]

values = dict()

i=0


for t in testdata.taskList:
    k=0
    y = []
    weightsY=[]
    for m in t.modeList:
        nameVar = str(i)+"t"+str(k) 
        point = LpVariable(name=nameVar,lowBound = 0,cat="Binary")
        y.append(point)
        values[m] = nameVar
        weightsY.append(m.q)
        k = k+1
    x.append(y)
    weightsX.append(weightsY)
    i=i+1

model+= lpSum(lpSum([x[s][v]*weightsX[s][v] for v in range(0,len(x[s]))] for s in range(0,len(x))))

i = 0

for t in testdata.taskList:
    model += lpSum(x[i][k] for k in range(0,len(t.modeList)))==1
    i = i+1


listOfALLModes = []

for t in testdata.taskList:
    for k in t.modeList:
        listOfALLModes.append(k)

listOfALLModes.sort(key=lambda x: x.p,reverse = True)

modesVisit = []
modesVariable = []

for t in listOfALLModes:
    p = values[t]
    coord = p.split("t")
    modesVariable.append(coord)
    modesVisit.append(t)

    model += lpSum([x[int(modesVariable[i][0])][int(modesVariable[i][1])] * modesVisit[i].comp for i in range(0,len(modesVisit))]) <=1

status  =model.solve()

#do some stuff
elapsed_time = time.perf_counter_ns() - timingStart

print(elapsed_time)

#print(f"status: {model.status}, {LpStatus[model.status]}")


#print(f"objective: {model.objective.value()}")



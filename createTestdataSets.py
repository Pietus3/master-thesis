import random
import pickle
from typing import Counter

class Mode:
    
    def __init__(self,id,c, t, d, q, p):
        self.comp = c
        self.interArrival = t
        self.relDeadline = d
        self.q = q
        self.p = p
        self.utilazation = round(self.comp / self.interArrival,3)
        self.id = id

    def printParameters(self):
        print("MODEID: " + str(self.id) + " \n Die WCET beträgt: "+ str(self.comp) + ", die inter-arrival Time beträgt: "
        + str(self.interArrival)+ ". die relative Deadline Beträgt: " + str(self.relDeadline) +". Der QoS-Value beträgt: " + str(self.q)+". Die Priorität des Modes liegt bei: "+ str(self.p))
    def printModeFormat(self):
        returnValue =[self.comp,self.interArrival,self.relDeadline,self.q,self.p,self.id,self.utilazation]
        return returnValue
        


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
    
    def printTaskFormat(self):
        returnValue =[]
        for taskMode in self.modeList:
            returnValue.append(taskMode.printModeFormat())
        return returnValue



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
    def printTaskSetFormat(self):
        returnValue =[]
        for task in self.taskList:
            returnValue.append(task.printTaskFormat())
        return returnValue


def createTestdata(cntTask,intModes, intQoS, floatWCET, maxPrio):
    tasks = []
    for k in cntTask:
        modes = []
        ranModes = random.randint(1,intModes)

        for i in range(0,ranModes):
            wcet = round(random.uniform(0.001,floatWCET),3)
            relDeadline =round(random.uniform(wcet,1),3)
            mode= Mode(str(k)+"t"+str(i),wcet,relDeadline,relDeadline,random.randint(0,intQoS),random.randint(0,maxPrio))
            modes.append(mode)
        
        tasks.append(Task(k,modes))
    
    return TaskSet(tasks)

def createTestdataFixedNumberTask(cntTask,intModes, intQoS, floatWCET, maxPrio):
    tasks = []
    for k in range(0,cntTask):
        
        indCount = 1
        innerTasks =[]
        for i in range(0,intModes):
            modes = []
            for k in range(0,indCount):
                wcet = round(random.uniform(0.001,floatWCET),3)
                relDeadline =round(random.uniform(wcet,1),3)
                mode= Mode(str(k)+"t"+str(i),wcet,relDeadline,relDeadline,random.randint(0,intQoS),random.randint(0,maxPrio))
                modes.append(mode)
            indCount= indCount +1
            innerTasks.append(modes)
        tasks.append(innerTasks)
    
    #print(tasks)

    return tasks

  #  taskSet = []

#    for taskComb in tasks:
#        for modeCount in range(0,len(taskComb)):
#            print(taskComb[modeCount])

        #print(taskComb)
#        print("NEW TASK")

     #   taskSet.append(Task(len(modes)modes))

def rekursiveCreationOfTestData(index,list,data):
    returnValue = []
    print("Startzustand des Returnvalues:")

    if len(list) == 0:
        #print(data[0])
        print("Initialisierung")
        for x in data[0]:
            taskList = [x]
            returnValue.append(taskList)
            
    else:
        for listElement in list:
            for dataElement in data[index]:
                tmp = listElement[:]
                tmp.append(dataElement)
                returnValue.append(tmp)

    if index == len(data)-1:
        return list
    else:
        print("Rekursion")
        return rekursiveCreationOfTestData(index+1,returnValue,data)
    


   # testSet.printTask()
  #  print(test[0])


def createFixedSet(cntTask,intModes, intQoS, floatWCET, maxPrio):
    testTasks = createTestdataFixedNumberTask(cntTask,intModes,intQoS,floatWCET,maxPrio)
    testList = []

    testSet =rekursiveCreationOfTestData(0,testList,testTasks)

    finalesSet = []

    for test in testSet:
        testSet =[]
        for task in test:
            finalesSet.append(Task(len(task),task))

    return TaskSet(finalesSet)


taskSets = []

for i in range(0,20):
    taskSets.append(createFixedSet(5,5,15,0.6,7).printTaskSetFormat())

with open('testSets.test', 'wb') as f:
    pickle.dump(taskSets,f)
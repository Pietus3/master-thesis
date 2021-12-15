import random
import pickle

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


def createTestdata(intTasks,intModes, intQoS, floatWCET, maxPrio):
    tasks = []
    for k in range(0,random.randint(1,intTasks)):
        modes = []
        ranModes = random.randint(1,intModes)

        for i in range(0,ranModes):
            wcet = round(random.uniform(0,floatWCET),3)
            relDeadline =random.uniform(0,wcet)
            mode= Mode(str(k)+"t"+str(i),wcet,round(relDeadline,3),round(relDeadline,3),random.randint(0,intQoS),random.randint(0,maxPrio))
            modes.append(mode)
        
        tasks.append(Task(k,modes))
    
    return TaskSet(tasks)


taskSets = []

for i in range(0,20):
    taskSets.append(createTestdata(5,5,15,0.6,7).printTaskSetFormat())

with open('readme.txt', 'wb') as f:
    pickle.dump(taskSets,f)
import logging

class Mode:
    
    def __init__(self,id,wcet, t, deadline, qos, priority, rdyTime,controlInstance):
        self.wcet = wcet
        self.interArrival = t 
        self.relDeadline = deadline
        self.qos = qos
        self.prior = priority
        self.utilazation = round(self.wcet / self.interArrival,3)
        self.id = id
        self.rdyTime = rdyTime
        self.progress= 0
        self.createdFollowingJob = False
        self.taskID = int(self.id.split("|")[0])
        self.controlInstance = controlInstance

    def makeControlInstance(self):
        self.controlInstance = True

    
    def work(self):
        self.progress = self.progress + 1
        if self.controlInstance and self.progress == self.wcet:
            return True
        else:
            return False


    def jobDone(self):
        return self.progress >= self.wcet

    def checkDeadlineMiss(self,timer):
        return timer > self.rdyTime+self.relDeadline
    
    def printMode(self):
        logging.info("[ID:" + str(self.id)+", WCET: "+ str(self.wcet) + ", interTime: "+str(self.interArrival) + ", relDeadline: "+str(self.relDeadline) + ", QoS: " + str(self.qos) 
            + ", Prior: "+ str(self.prior) +", rdyTime: "+ str(self.rdyTime) + ",Progress: "+str(self.progress)+ "]")

    def printModeConsole(self):
        print("[ID:" + str(self.id)+", WCET: "+ str(self.wcet) + ", interTime: "+str(self.interArrival) + ", relDeadline: "+str(self.relDeadline) + ", QoS: " + str(self.qos) 
            + ", Prior: "+ str(self.prior) +", rdyTime: "+ str(self.rdyTime) + ",Progress: "+str(self.progress)+ "]")
    
    def printModeFormat(self):
        returnValue =[self.comp,self.interArrival,self.relDeadline,self.q,self.p,self.id,self.utilazation]
        return returnValue
        


class Task:
    def __init__(self, id, modes,active,controlInstance):
        self.id = id
        self.modeList = []
        self.isActive = active
        self.activeMode = 0
        self.controlInstance = controlInstance

        for mode in modes:
            if self.controlInstance:
                mode.makeControlInstance()
            self.modeList.append(mode)

    def getActiveMode(self):
        return self.modeList[self.activeMode]
    
    def changeActiveMode(self, id):
        self.activeMode = id
    
    def printTask(self):
        print("TASKID" + str(self.id))
        for mode in self.modeList:
            mode.printModeConsole()

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
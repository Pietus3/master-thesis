import logging
from re import split
from TaskClasses import Mode
from MultiModeChoice import ILP,Greedy


class EventBasedSimulator:
    
    def __init__(self,tasks,events):
        self.taskList = tasks
        self.activeTasks = None
        self.passiveTasks = None
        self.readyList = None
        self.blockedList = None
        self.eventList = events
        self.runningJob = None
        self.timer = 0
        self.SolverGreedy = True

    def executeModeChoice(self,greedy):
        if greedy:
            Solver = Greedy(self.activeTasks)
        else:
            Solver= ILP(self.activeTasks)

       # print("PRE ALGO")
       # for element in self.activeTasks:
       #     element.printTask()

        chosenModes = Solver.generate()

       # print("AFTER ALGO")
       # for element in self.activeTasks:
       #     element.printTask()
        

        for id in chosenModes:
            splittedID = id.split("|")
            self.taskList[int(splittedID[0])].activeMode = int(splittedID[1])

    def initilizeSimulator(self):
        logging.info("INITILAZATION OF THE SIMULATOR")

        self.activeTasks = [task for task in self.taskList if task.isActive]
        self.passiveTasks = [task for task in self.taskList if not task.isActive]

        self.executeModeChoice(self.SolverGreedy)

        self.readyList = [task.getActiveMode() for task in self.taskList if task.getActiveMode().rdyTime <= self.timer]
        self.blockedList = [task.getActiveMode() for task in self.taskList if task.getActiveMode().rdyTime > self.timer]

        self.readyList = sorted(self.readyList, key=lambda x: x.prior,reverse= True)
        self.blockedList = sorted(self.blockedList, key=lambda x: x.prior)

        self.newRunningJob()

    def newRunningJob(self):
        logging.info("NEW RUNNING JOB")
    
        if self.readyList:
            newRunningJob = self.readyList.pop(0)
            self.runningJob = newRunningJob
            #IF Abfrage für den Fall das Task vorher verdrängt wurde, ansonsten zuviele Following Jobs
            
            if not self.runningJob.createdFollowingJob:
                newMode = self.taskList[newRunningJob.taskID].getActiveMode()
                newModeInstance = Mode(newMode.id,newMode.wcet,
                    newMode.interArrival,newMode.relDeadline,
                    newMode.qos,newMode.prior,0)
                newModeInstance.rdyTime = newRunningJob.rdyTime + newRunningJob.interArrival

                self.blockedList.append(newModeInstance)
                self.runningJob.createdFollowingJob = True
                self.blockedList = sorted(self.blockedList, key=lambda x: x.rdyTime)
        else:
            logging.info("READYLIST EMPTY" + str(len(self.readyList)))
            self.runningJob = None

    def higherPrioAwaked(self):
        newRunningJob = self.readyList.pop(0)
        self.readyList.insert(0,self.runningJob)
        self.readyList = sorted(self.readyList, key=lambda x: x.prior,reverse= True)
        self.runningJob = newRunningJob
        self.blockedList.append(Mode(newRunningJob.id,newRunningJob.wcet,
                newRunningJob.interArrival,newRunningJob.relDeadline,
                newRunningJob.qos,newRunningJob.prior,self.timer+newRunningJob.interArrival))
        self.blockedList = sorted(self.blockedList, key=lambda x: x.rdyTime)

    def getRunningJob(self):
        return self.runningJob

    def jobProgress(self):
        if self.runningJob is None:
            logging.info("NOTHING TO RUN")           
        else:
            logging.info("JOB PROGRESS")
            if self.runningJob.jobDone():
                self.newRunningJob()
            if self.runningJob is not None:
                self.runningJob.work()

    def checkForReadyTasks(self):
        added = False
        toRemove = []
        for elem in self.blockedList:            
            if elem.rdyTime <= self.timer:
                toRemove.append(elem)
                self.readyList.append(elem)
                added = True
            
        for elem in toRemove:
                self.blockedList.remove(elem)    

        if added:
            self.readyList = sorted(self.readyList, key=lambda x: x.prior,reverse= True)
            if self.runningJob is None:
                self.newRunningJob()
            if len(self.readyList)>0:
                if self.runningJob.prior < self.readyList[0].prior:
                    self.higherPrioAwaked()
            
    def printSimulatorState(self):
        logging.info("TIMING" + str(self.timer))
        logging.info("RUNNING MODE")
        if self.runningJob is not None:
            self.runningJob.printMode()
        else:
            logging.info("NO RUNNING MODE")
        logging.info("READYLIST")
        for elem in self.readyList:
                elem.printMode()
        logging.info("BLOCKEDLIST")
        for elem in self.blockedList:
                elem.printMode()
        logging.info("----------------------------------------------------------------")

    def checkModeValidation(self):
        self.executeModeChoice(self.SolverGreedy)

    def checkEvents(self):
        deleteEvent = []
        for event in self.eventList:
            if event.timestamp ==self.timer:
                for action in event.actionList:
                    action.run()
                deleteEvent.append(event)
                self.checkModeValidation()
        for delEvent in deleteEvent:
            self.eventList.remove(delEvent)

    def checkDeadlineMisses(self):
        for m in self.readyList:
            if m.checkDeadlineMiss(self.timer):
                print("DEADLINE WURDE VERPASST at time: "+ str(self.timer))
                exit()
        
        if self.runningJob:
            if self.runningJob.checkDeadlineMiss(self.timer):
                print("DEADLINE MISSED at time: " + str(self.timer))
                exit()


    def tick(self):
        self.printSimulatorState()

        self.timer = self.timer + 1
        self.checkEvents()
        self.checkForReadyTasks()
        self.jobProgress()
        self.checkDeadlineMisses()
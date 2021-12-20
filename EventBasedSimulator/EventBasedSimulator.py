from TaskClasses import Mode
from MultiModeChoice import ILP


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

    def initilizeSimulator(self):
        print("INIT")

        self.activeTasks = [task for task in self.taskList if task.isActive]
        self.passiveTasks = [task for task in self.taskList if not task.isActive]

        self.readyList = [task.getActiveMode() for task in self.taskList if task.getActiveMode().rdyTime <= self.timer]
        self.blockedList = [task.getActiveMode() for task in self.taskList if task.getActiveMode().rdyTime > self.timer]

        self.readyList = sorted(self.readyList, key=lambda x: x.prior,reverse= True)
        self.blockedList = sorted(self.blockedList, key=lambda x: x.prior)

       # Test = ILP(self.activeTasks)
       # Test.generate()

        self.newRunningJob()

    def newRunningJob(self):
        print("NEW RUNNING JOB")
    
        if self.readyList:
            newRunningJob = self.readyList.pop(0)
            self.runningJob = newRunningJob
            #IF Abfrage für den Fall das Task vorher verdrängt wurde, ansonsten zuviele Following Jobs
            
            if not self.runningJob.createdFollowingJob:
                self.blockedList.append(Mode(newRunningJob.id,newRunningJob.wcet,
                    newRunningJob.interArrival,newRunningJob.relDeadline,
                    newRunningJob.qos,newRunningJob.prior,self.timer+newRunningJob.interArrival))
                self.runningJob.createdFollowingJob = True
                self.blockedList = sorted(self.blockedList, key=lambda x: x.rdyTime)
        else:
            print("READYLIST EMPTY" + str(len(self.readyList)))
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
            print("NOTHING TO RUN")           
        else:
            print("JOB PROGRESS")
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
        print("TIMING" + str(self.timer))
        print("RUNNING MODE")
        if self.runningJob is not None:
            self.runningJob.printMode()
        else:
            print("NO RUNNING MODE")
        print("READYLIST")
        for elem in self.readyList:
                elem.printMode()
        print("BLOCKEDLIST")
        for elem in self.blockedList:
                elem.printMode()
        print("----------------------------------------------------------------")

    def checkEvents(self):
        deleteEvent = []
        for event in self.eventList:
            if event.timestamp ==self.timer:
                for action in event.actionList:
                    action.run()
                deleteEvent.append(event)
        for delEvent in deleteEvent:
            self.eventList.remove(delEvent)


    def tick(self):
        self.printSimulatorState()

        self.timer = self.timer + 1
        self.checkEvents()
        self.checkForReadyTasks()
        self.jobProgress()
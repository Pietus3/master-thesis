from os import remove
from EventBasedSimulator import EventBasedSimulator
from TaskClasses import Mode
import logging

class Event:
    
    def __init__(self,timestamp,actions):
        self.timestamp = timestamp
        self.actionList =actions

class Action():
    def __init__(self,id,eventBasedSimulator):
        self.id = id
        self.eventBasedSimulator = eventBasedSimulator
        

class ChangeQoS(Action):
    def __init__(self,id,eventBasedSimulator,modeID, newQoS):
        super().__init__(id,eventBasedSimulator)
        self.targetModeID = modeID
        self.newQoS = newQoS

    def run(self):
        value = self.targetModeID.split("|")
        logging.info("QOSEvent ----- ZielTask: "+ str(value[0]) + ">>>> ZielMode: " + str(value[1]) +" >>> Neuer QoS-Value: " + str(self.newQoS))

        self.eventBasedSimulator.taskList[int(value[0])].modeList[int(value[1])].qos = self.newQoS

class ChangeStat(Action):
    def __init__(self, id,eventBasedSimulator,taskId,active):
        super().__init__(id,eventBasedSimulator)
        self.taskId = taskId
        self.active = active

    def run(self):
        logging.info("STATCHANGE EVENT ----- ZielTask: "+ str(self.taskId) + " >>> Neuer  STATE " + str(self.active))
       

        if self.active:
            sim = self.eventBasedSimulator

            sim.activeTasks.append(sim.taskList[self.taskId])
            sim.passiveTasks.remove(sim.taskList[self.taskId])

            task = sim.taskList[self.taskId]
            task.activeMode = len(task.modeList)-1

            infos = sim.taskList[self.taskId].getActiveMode()

            newMode = Mode(infos.id,infos.wcet,infos.interArrival,infos.relDeadline,infos.qos,infos.prior,0)
            newMode.rdyTime = sim.timer
            newMode.progress = 0

            sim.readyList.append(newMode)
            sim.readyList  = sorted(sim.readyList, key=lambda x: x.prior,reverse= True)
        
            if sim.runningJob:
                if newMode.prior > sim.runningJob.prior:
                    sim.higherPrioAwaked()
        
        
        else:
            sim = self.eventBasedSimulator
     
            sim.activeTasks.remove(sim.taskList[self.taskId])
            sim.passiveTasks.append(sim.taskList[self.taskId])
            
            removeReadyModes =[]
            removeBlockedModes = []

            for mode in sim.readyList:
                if mode.taskID == self.taskId:
                    removeReadyModes.append(mode)
            
            for mode in sim.blockedList:
                if mode.taskID == self.taskId:
                    removeBlockedModes.append(mode)

            for item in removeReadyModes:
                sim.readyList.remove(item)

            for item in removeBlockedModes:
                sim.blockedList.remove(item)
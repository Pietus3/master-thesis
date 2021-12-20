from EventBasedSimulator import EventBasedSimulator


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
        print("ZielTask: "+ str(value[0]) + "ZielMode: " + str(value[1]))

        self.eventBasedSimulator.taskList[int(value[0])].modeList[int(value[1])].qos = self.newQoS

class ChangeStat(Action):
    def __init__(self, id,eventBasedSimulator):
        super().__init__(id,eventBasedSimulator)

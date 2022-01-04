import random
from TaskClasses import Mode,Task,TaskSet

class TestDataCreater():

    def createTestdata(self,cntTask,intModes, intQoS, floatWCET, maxPrio):
        tasks = []
        for k in range(0,cntTask):
            modes = []
            ranModes = random.randint(1,intModes)

            for i in range(0,ranModes):
                wcet = round(random.uniform(0.001,floatWCET),3)
                relDeadline =round(random.uniform(wcet,1),3)
                mode= Mode(str(k)+"|"+str(i),wcet,relDeadline,relDeadline,random.randint(0,intQoS),random.randint(0,maxPrio),0)
                modes.append(mode)
        
            tasks.append(Task(k,modes,True))
    
        return TaskSet(tasks)

    def createTaskSet(self, cntSets, cntTask, cntMaxModes, intQoS, floatWCET,maxPrio):
        returnValue = []
        for i in range(0,cntSets):
            randomModes = random.randint(1,cntMaxModes)
            returnValue.append(self.createTestdata(cntTask,randomModes,intQoS,floatWCET,maxPrio))
        return returnValue


    def createTestdataFixedModes(self,cntTask,fixedModes, intQoS, floatWCET, maxPrio):
        tasks = []
        for k in range(0,cntTask):
            modes = []
            for i in range(0,fixedModes):
                wcet = round(random.uniform(0.001,floatWCET),3)
                relDeadline =round(random.uniform(wcet,1),3)
                mode= Mode(str(k)+"|"+str(i),wcet,relDeadline,relDeadline,random.randint(0,intQoS),random.randint(0,maxPrio),0)
                modes.append(mode)
        
            tasks.append(Task(k,modes,True))
    
        return TaskSet(tasks)

    def createTaskSetFixedModesCount(self,cntSets,cntTask,cntMaxModes,intQoS,floatWCET,maxPrio):
        returnValue = []

        for i in range(1,cntTask):
            for k in range(0,cntSets):
                returnValue.append(self.createTestdataFixedModes(i,cntMaxModes,intQoS,floatWCET,maxPrio))
        
        return returnValue
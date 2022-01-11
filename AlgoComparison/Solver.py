import logging
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from pulp import PULP_CBC_CMD
from pulp.utilities import value
import pulp
import time
from TaskClasses import Mode,Task

class ILP:
    def __init__(self, taskSet) -> None:
        self.taskSet = taskSet 
    
    def generate(self):
        timingStart = time.perf_counter_ns()
        
        model = LpProblem(name="small-problem", sense=LpMaximize)

        xVariable = dict()
        weightsX= dict()

        allModes = []

        for task in self.taskSet:
            yVariable = dict()
            weightsY=dict()
            for m in task.modeList:

                allModes.append(m)
                nameVar = m.id.split("|")
                point = LpVariable(name=m.id,lowBound = 0,cat="Binary")
                yVariable[nameVar[1]]= point
                weightsY[nameVar[1]] = m.qos
            xVariable[nameVar[0]]=yVariable
            weightsX[nameVar[0]] = weightsY

        model+= lpSum(lpSum(xVariable[m.id.split("|")[0]][m.id.split("|")[1]]*weightsX[m.id.split("|")[0]][m.id.split("|")[1]] for m in allModes))

        i = 0
        for t in self.taskSet:
            model += lpSum(xVariable[m.id.split("|")[0]][m.id.split("|")[1]] for m in t.modeList)==1
            i = i+1

        model += lpSum(lpSum(xVariable[m.id.split("|")[0]][m.id.split("|")[1]] * m.utilazation for m in task.modeList) for task in self.taskSet) <=1


        status  = model.solve(PULP_CBC_CMD(msg=False))

        elapsed_time = time.perf_counter_ns() - timingStart

        countTask = len(self.taskSet)

        countMode = sum([len(task.modeList) for task in self.taskSet])


        eva = (model.objective.value(),elapsed_time/1000,countTask,countMode,model.status)
        
        if model.status:
            choosenModes =[]
            for var in model.variables():
                if var.value():
                    choosenModes.append(var.name)

            return (choosenModes,eva)

class Greedy:
    def __init__(self,taskSet) -> None:
        self.taskSet = taskSet
    def generate(self):
        countTask = len(self.taskSet)

        countMode = sum([len(task.modeList) for task in self.taskSet])

        for task in self.taskSet:
            task.modeList.sort(key=lambda x: x.utilazation,reverse = True)

        timingStart = time.perf_counter_ns()

        valid = 1 

        while sum(number.modeList[0].utilazation for number in self.taskSet) >1:
            biggestCriteria = -1
            biggestCriteriaIndex = -1
            index = 0
            for task in self.taskSet:
                if len(task.modeList)>1 and task.modeList[0].utilazation > biggestCriteria:
                    biggestCriteria = task.modeList[0].utilazation
                    biggestCriteriaIndex =index
                index = index + 1

            if biggestCriteriaIndex != -1:
                del self.taskSet[biggestCriteriaIndex].modeList[0]     
            else:
                valid = -1
                break


        for task in self.taskSet:
            task.modeList.sort(key=lambda x: x.qos,reverse = True)
        
        choosenModes = []

        for task in self.taskSet:
            choosenModes.append(task.modeList[0].id)
            
        elapsed_time = time.perf_counter_ns() - timingStart

        sumQoS = sum([task.modeList[0].qos for task in self.taskSet])

        eva = (sumQoS,elapsed_time/1000,countTask,countMode,valid)
        
        return (choosenModes,eva)
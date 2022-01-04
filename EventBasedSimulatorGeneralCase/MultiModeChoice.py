import logging
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
from pulp import PULP_CBC_CMD
from pulp.utilities import value
import pulp

class ILP:
    def __init__(self, taskSet) -> None:
        self.taskSet = taskSet 
    
    def generate(self):
        model = LpProblem(name="small-problem", sense=LpMaximize)

        xVariable = dict()
        weightsX= dict()

        i=0

        allModes = []

        for task in self.taskSet:
            k=0
            yVariable = dict()
            weightsY=dict()
            for m in task.modeList:

                allModes.append(m)
                nameVar = m.id.split("|")
                point = LpVariable(name=m.id,lowBound = 0,cat="Binary")
                yVariable[nameVar[1]]= point
                weightsY[nameVar[1]] = m.qos# finde Value Stell
                k = k+1
            xVariable[nameVar[0]]=yVariable
            weightsX[nameVar[0]] = weightsY
            i=i+1

        model+= lpSum(lpSum(xVariable[m.id.split("|")[0]][m.id.split("|")[1]]*weightsX[m.id.split("|")[0]][m.id.split("|")[1]] for m in allModes))

        i = 0
        for t in self.taskSet:
            model += lpSum(xVariable[m.id.split("|")[0]][m.id.split("|")[1]] for m in t.modeList)==1
            i = i+1
        modesVisit = []

        for task in self.taskSet:
            for mode in task.modeList: 
                modesVisit.append(mode)
                model += lpSum(xVariable[m.id.split("|")[0]][m.id.split("|")[1]] * m.utilazation for m in modesVisit) <=1
            

        status  =model.solve(PULP_CBC_CMD(msg=False))

        #print(f"status: {model.status}, {LpStatus[model.status]}")

        #for var in model.variables():
        #    print(f"{var.name}: {var.value()}")
        
        if model.status:
            logging.info("Es existiert eine optimale Lösung")
            choosenModes =[]
            for var in model.variables():
                if var.value():
                    choosenModes.append(var.name)

            return choosenModes

class Greedy:
    def __init__(self,taskSet):
        self.taskSet = taskSet
    
    def generate(self):
        for task in self.taskSet:
            task.modeList.sort(key=lambda x: x.utilazation,reverse = True)

        while sum(number.modeList[0].utilazation for number in self.taskSet) >1:
            biggestCriteria = -1
            biggestCriteriaIndex = -1
            index = 0
            for task in self.taskSet:
                if len(task)>1 and task[0].utilazation > biggestCriteria:
                    biggestCriteria = task[0].utilazation
                    biggestCriteriaIndex =index
                index = index + 1

            if biggestCriteriaIndex != -1:
                del self.taskSet[biggestCriteriaIndex][0]     
            else:
                break


        for task in self.taskSet:
            task.modeList.sort(key=lambda x: x.qos,reverse = True)
        
        choosenModes = []

        for task in self.taskSet:
            choosenModes.append(task.modeList[0].id)
        #    print(task.modeList[0].id)
            task.modeList.sort(key=lambda x: x.id,reverse = False)
            
        return choosenModes
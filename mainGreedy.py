import pickle

STATIC_VARIABLEUTILAZATION = 6


with open("readme.txt", "rb") as fp:   # Unpickling
    taskSets = pickle.load(fp)

# Prepare Data

for task in taskSets[0]:
    task.sort(key=lambda x: x[STATIC_VARIABLEUTILAZATION],reverse = True)


for task in taskSets[0]:
    print(task)



while sum(number[0][STATIC_VARIABLEUTILAZATION] for number in taskSets[0]) >1:
    biggestCriteria = -1
    biggestCriteriaIndex = -1
    index = 0
    for task in taskSets[0]:
        if len(task)>1 and task[0][STATIC_VARIABLEUTILAZATION] > biggestCriteria:
            biggestCriteria = task[0][STATIC_VARIABLEUTILAZATION]
            biggestCriteriaIndex =index
        index = index + 1

    if index != -1:
        del taskSets[0][biggestCriteriaIndex][0]     
        print("Element wurde entfernt")
    else:
        print("Es konnte kein Element entfernt werden")
        exit()

print("Es wurde ein funktionierendes System erzeugt")

for task in taskSets[0]:
    print(task)
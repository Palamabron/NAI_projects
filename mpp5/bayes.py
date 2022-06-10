from dataManipulation import *


def countPossibility(pointList, twoDList, alpha=1):
    if len(pointList) != len(twoDList[0]) - 1:
        return "error"
    labelsList = getValuesSet(twoDList)
    decisionDict = getDecisionDict(twoDList)
    decisionsCount = [0 for _ in range(len(decisionDict))]
    countValues = [[0 for _ in range(len(twoDList[0]) - 1)] for _ in range(len(decisionDict))]
    possibilities = [0.0 for _ in range(len(decisionsCount))]
    result = ""
    for i in range(len(twoDList)):
        for decision in decisionDict.keys():
            if decision == twoDList[i][-1]:
                decisionsCount[decisionDict[decision]] += 1
                for j in range(len(twoDList[i]) - 1):
                    if pointList[j] == twoDList[i][j]:
                        countValues[decisionDict[decision]][j] += 1
    # print(f'DecisionsCount: {decisionsCount}')
    for i in range(len(possibilities)):
        possibilities[i] = decisionsCount[i] / sum(decisionsCount)
        for j in range(len(countValues)):
            if countValues[i][j] == 0:
                possibilities[i] *= alpha / (decisionsCount[i] + alpha * len(labelsList[j]))
            else:
                possibilities[i] *= countValues[i][j] / decisionsCount[i]
    result += f"{pointList}:\n"
    for i in range(len(possibilities)):
        result += f"\t{list(decisionDict.keys())[i]}: {round(possibilities[i] * 100, 2)}%\n"
    return result


def testData(testTwoDList, trainTwoDList, alpha=1):
    for vector in testTwoDList:
        vectorPrediction = countPossibility(vector, trainTwoDList, alpha)
        print(vectorPrediction)
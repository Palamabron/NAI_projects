def fileToTwoDList(fileContent, separator=','):
    fileContent = fileContent.rstrip()
    if separator != ',':
        fileContent = fileContent.replace(',', '.')
    fileContent = fileContent.split('\n')
    for i in range(len(fileContent)):
        fileContent[i] = fileContent[i].split(separator)
    for i in range(len(fileContent)):
        for j in range(len(fileContent[i])):
            if '.' in fileContent[i][j]:
                fileContent[i][j] = float(fileContent[i][j])
    return fileContent


def getValuesSet(twoDList):
    values = []
    for i in range(len(twoDList[0])):
        column = set([row[i] for row in twoDList])
        values.append(list(column))
    return values


def getDecisionDict(twoDList):
    decisionsDict = {}
    decisionSet = [twoDList[0][-1]]
    for i in range(len(twoDList)):
        if twoDList[i][-1] not in decisionSet:
            decisionSet.append(twoDList[i][-1])
    for i in range(len(decisionSet)):
        decisionsDict[i] = decisionSet[i]
    decisionsDict = {v: k for k, v in decisionsDict.items()}
    return decisionsDict

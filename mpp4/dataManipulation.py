
def fileToTwoDList(fileContent, separator):
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


def deleteLabelFromData(twoDList):
    labelIndex = getLabelIndex(twoDList)
    for i in range(len(twoDList)):
        del twoDList[i][labelIndex]
    return twoDList


def getLabelIndex(twoDList):
    for i in range(len(twoDList[0])):
        if isinstance(twoDList[0][i], str):
            return i
    return len(twoDList[0]) - 1


def getLabelsList(twoDList):
    labelIndex = getLabelIndex(twoDList)
    labels = []
    for row in twoDList:
        if row[labelIndex] not in labels:
            labels.append(row[labelIndex])
    return labels

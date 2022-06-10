import random
import matplotlib.pyplot as plt


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


def plotList(twoDList):
    atribIndex = findAtribIndex(twoDList)
    atribSet = list(set([row[atribIndex] for row in twoDList]))
    distinctColors = ['grey', 'olive', 'purple', 'green', 'brown', 'red', 'orange', 'blue']
    result = []
    plotIndex = 0
    for _ in range(len(atribSet)):
        result.append([])
    for i in range(len(twoDList[0])):
        for j in range(len(twoDList[0])):
            if j != atribIndex and i != atribIndex and i < j:
                plt.figure(plotIndex).canvas.manager.set_window_title('Data Comparison')
                colors = random.sample(distinctColors, len(atribSet))
                atribs = [el[atribIndex] for el in twoDList]
                tmp1 = [el[j] for el in twoDList]
                tmp2 = [el[i] for el in twoDList]
                for h in range(len(tmp1)):
                    for k in range(len(atribSet)):
                        if atribs[h] == atribSet[k]:
                            result[k].append((tmp1[h], tmp2[h], colors[k]))
                for k in range(len(result)):
                    x = [row[0] for row in result[k]]
                    y = [row[1] for row in result[k]]
                    c = result[k][0][2]
                    # print(f"x{k}: {len(x)}")
                    # print(f"y{k}: {len(y)}")
                    plt.scatter(x, y, color=c)
                    plt.legend([el for el in atribSet])
                for h in range(len(result)):
                    result[h].clear()
                plt.title(f'Comparing {i + 1} column with {j + 1} column')
                plotIndex += 1
    plt.show()


def plotK(testList, trainList):
    kList = []
    accuracies = []
    plt.figure('K plot')
    for i in range(1, 11):
        accuracies.append(testEval(testList, trainList, i))
        kList.append(i)
    plt.plot(kList, accuracies)
    plt.title('Accuracy to number of neighbors')
    plt.show()


def checkVector(vector, trainList, k):
    distances, atribValues = [], []
    dst = 0.0
    atribIndex = findAtribIndex(trainList)

    for trainRow in trainList:
        for i in range(len(trainRow)):
            if isinstance(trainRow[i], float):
                atribValues.append(trainRow[i])
        for i in range(len(atribValues)):
            dst += (atribValues[i] - vector[i]) ** 2
        atribValues.clear()
        distances.append((round(dst, 4), trainRow[atribIndex]))
        dst = 0.0
    distances = sorted(distances, key=lambda x: x[0])
    neighbors = distances[0:k]
    neighbors = [neighbor[1] for neighbor in neighbors]
    label = max(set(neighbors), key=neighbors.count)
    # print(f"Predicted label for vector {vector}: {label}")
    # distances = []
    return label


def findAtribIndex(dataList):
    for i in range(len(dataList[0])):
        if isinstance(dataList[0][i], str):
            atribIndex = i
            return atribIndex
    return len(dataList[0]) - 1


def testEval(testList, trainList, k):
    distances = []
    dst = 0.0
    atribIndex = findAtribIndex(trainList)
    correct = 0
    for tmpIndex in range(len(testList)):
        for trainRow in trainList:
            for i in range(len(trainRow)):
                if isinstance(trainRow[i], float):
                    dst += (trainRow[i] - testList[tmpIndex][i]) ** 2
            distances.append((round(dst, 4), trainRow[atribIndex]))
            dst = 0.0
        distances = sorted(distances, key=lambda x: x[0])
        neighbors = distances[0:k]
        neighbors = [neighbor[1] for neighbor in neighbors]
        label = max(set(neighbors), key=neighbors.count)
        print(f"{tmpIndex+1}: predicted label: {label}, expected: {testList[tmpIndex][atribIndex]}")
        if label == testList[tmpIndex][atribIndex]:
            correct += 1
        distances = []
    accuracy = correct / len(testList)
    print(f'Accuracy: {round(accuracy, 5) * 100}%')
    return accuracy

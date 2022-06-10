import copy
import math
import random
import matplotlib.pyplot as plt


def createCentroids(testData, k):
    attribNumber = len(testData[0])
    centroids = random.sample(testData, k)
    for point in testData:
        scalarsDistances = [[0.0 for _ in range(len(centroids[i]))] for i in range(len(centroids))]
        distances = [0.0 for _ in range(len(centroids))]
        for i in range(len(centroids)):
            for j in range(attribNumber):
                scalarsDistances[i][j] += (point[j] - centroids[i][j]) ** 2
        for i in range(len(scalarsDistances)):
            for j in range(len(scalarsDistances[i])):
                distances[i] += scalarsDistances[i][j]
            distances[i] = math.sqrt(distances[i])
        closestCentroidIndex = distances.index(min(distances))
        testData[testData.index(point)].append(closestCentroidIndex)
    return testData


def calculateAverageCoords(testData, k):
    centroidAverages = [[0.0 for _ in range(len(testData[0]) - 1)] for _ in range(k)]
    clustersSizes = [0] * k
    for i in range(len(testData)):
        for j in range(len(testData[i]) - 1):
            centroidAverages[testData[i][-1]][j] += testData[i][j]
        clustersSizes[testData[i][-1]] += 1

    for i in range(len(centroidAverages)):
        for j in range(len(centroidAverages[i])):
            centroidAverages[i][j] /= clustersSizes[i]

    return centroidAverages


def reCluster(testData, centroidAverages):
    # print(testData, end='\n######################\n')
    # print('###################################')
    for i in range(len(testData)):
        scalarsDifferences = [[0.0 for _ in range(len(centroidAverages[i]))] for i in range(len(centroidAverages))]
        errors = [0.0 for _ in range(len(centroidAverages))]
        for j in range(len(centroidAverages)):
            for k in range(len(centroidAverages[j])):
                scalarsDifferences[j][k] += (testData[i][k] - centroidAverages[j][k]) ** 2
        for j in range(len(centroidAverages)):
            for k in range(len(centroidAverages[j])):
                errors[j] += scalarsDifferences[j][k]
            errors[j] = math.sqrt(errors[j])
        nextCentroidIndex = errors.index(min(errors))
        # print(f'Previously: {testData[i][-1]} Now: {nextCentroidIndex}')
        testData[i][-1] = nextCentroidIndex
    # print(testData)
    return testData.copy()


def checkVector(vector, centroids):
    distances = [0.0] * len(centroids)
    for i in range(len(centroids)):
        for j in range(len(centroids[i])):
            distances[i] += (vector[j] - centroids[i][j]) ** 2
    closestCentroid = centroids[centroids.index(min(distances))]
    return closestCentroid


def plotDataPoints(testData, centroidAverages):
    distinctColors = ['grey', 'olive', 'purple', 'green', 'brown', 'red', 'orange', 'blue']
    result = [[] for _ in range(len(centroidAverages))]
    plotIndex = 0
    for i in range(len(testData[0]) - 1):
        for j in range(len(testData[0]) - 1):
            if i < j:
                plt.figure(plotIndex).canvas.manager.set_window_title('Data Comparison')
                colors = random.sample(distinctColors, len(centroidAverages))
                attribs = [el[-1] for el in testData]
                tmp1 = [el[j] for el in testData]
                tmp2 = [el[i] for el in testData]
                for h in range(len(tmp1)):
                    for k in range(len(centroidAverages)):
                        if attribs[h] == list(range(len(centroidAverages)))[k]:
                            result[k].append((tmp1[h], tmp2[h], colors[k]))
                for k in range(len(result)):
                    x = [row[0] for row in result[k]]
                    y = [row[1] for row in result[k]]
                    c = result[k][0][2]
                    # print(f"x{k}: {len(x)}")
                    # print(f"y{k}: {len(y)}")
                    plt.scatter(x, y, color=c)
                    # plt.legend([el for el in list(range(len(centroidAverages)))])
                for h in range(len(result)):
                    result[h].clear()
                plt.title(f'Comparing {i + 1} column with {j + 1} column')
                plotIndex += 1
    plt.show()


def getCurrentCentroids(testData, centroidAverages):
    currentCentroids = []
    minimums = [[] for _ in range(len(centroidAverages))]
    minimumsIndex = [[] for _ in range(len(centroidAverages))]
    for i in range(len(testData)):
        tmp = 0.0
        for j in range(len(testData[i]) - 1):
            tmp += (testData[i][j] - centroidAverages[testData[i][-1]][j]) ** 2
        minimums[testData[i][-1]].append(tmp)
        minimumsIndex[testData[i][-1]].append(i)
    for i in range(len(minimums)):
        minimumIndex = minimumsIndex[i][minimums[i].index(min(minimums[i]))]
        currentCentroids.append(testData[minimumIndex])
    return currentCentroids


def innerClusterDistance(testData, centroids):
    bigE = 0.0
    for i in range(len(testData)):
        for centroid in centroids:
            if testData[i][-1] == centroid[-1]:
                for j in range(len(testData[i]) - 1):
                    bigE += (centroid[j] - testData[i][j]) ** 2
    return bigE


def calculateCentroids(data_list, k):
    # data = deleteLabelFromData(data_list)
    data = data_list
    clustered_data_list = createCentroids(copy.deepcopy(data), k)
    centroidAverages = calculateAverageCoords(copy.deepcopy(clustered_data_list), k)
    prevClustered = copy.deepcopy(clustered_data_list)
    E1 = -1
    reClustered = reCluster(copy.deepcopy(prevClustered), centroidAverages)
    # print(prevClustered)
    E2 = innerClusterDistance(reClustered, getCurrentCentroids(reClustered, centroidAverages))
    print(reClustered)
    i = 0
    distanceDivHistory = [E1, E2]
    print(f'{i + 1}. E = {distanceDivHistory[i]}')
    while distanceDivHistory[-1] != distanceDivHistory[-2]:
        # print('###################################')
        print(f'{i+2}. E = {distanceDivHistory[-1]}')
        prevClustered = copy.deepcopy(reClustered)
        prevDistance = innerClusterDistance(prevClustered, getCurrentCentroids(reClustered, centroidAverages))
        if prevDistance > distanceDivHistory[-1]:
            break
        distanceDivHistory.append(prevDistance)
        centroidAverages = calculateAverageCoords(reClustered, k)
        reClustered = reCluster(reClustered, centroidAverages)
        reDistance = innerClusterDistance(reClustered, getCurrentCentroids(reClustered, centroidAverages))
        if reDistance > distanceDivHistory[-1]:
            break
        distanceDivHistory.append(reDistance)
        i += 1
        # print(reClustered)
    print(reClustered)
    return centroidAverages, reClustered

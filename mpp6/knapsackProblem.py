def txtToKnapsack(path="Data/plecak.txt"):
    with open(path) as file:
        data = file.read()
    data = data.split('\n')
    data[0] = data[0].split(' ')
    data[0][0] = int(data[0][0])
    data[0][1] = int(data[0][1])
    for i in range(1, len(data)):
        data[i] = data[i].split(',')
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
    # print(data)
    return data


def getItemDict(weights, values):
    resultDict = {}
    for i in range(len(weights)):
        resultDict.update({weights[i]: values[i]})


def knapsack(Capacity, weights, values):
    if len(weights) != len(values):
        print("Error: Length of values and weights list is not the same")
        return
    bestVectorFound = None
    bestFoundWeight = 0
    bestFoundValue = 0
    for i in range(1, 2 ** len(weights)):
        permutation = "{0:b}".format(i)
        permutation = permutation.zfill(len(weights))
        totalWeight = 0
        totalValue = 0
        for j, char in enumerate(permutation):
            if char == '1':
                totalWeight += weights[j]
                totalValue += values[j]
                if totalWeight > Capacity:
                    break
        if totalWeight > Capacity:
            continue
        else:
            if totalValue > bestFoundValue or bestFoundValue == 0:
                permutation = [int(c) for i, c in enumerate(permutation)]
                bestVectorFound = permutation
                bestFoundValue = totalValue
                bestFoundWeight = totalWeight
                print(
                    f"{i}. New best vector has been found: {bestVectorFound}, weightSum: {totalWeight}, valueSum: {totalValue}")
    print(
        f"At the end the best found vector is {bestVectorFound} with weightSum {bestFoundWeight} and valueSum: {bestFoundValue}")

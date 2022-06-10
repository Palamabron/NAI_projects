def getData(path="Data/huffman.txt"):
    with open(path) as file:
        data = file.read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(" ")
        data[i][-1] = int(data[i][-1])
    # print(data)
    return data


def dataToSortedDict(data):
    letterDict = {}
    for i in range(len(data)):
        if i > 0:
            letterDict[data[i][0]] = data[i][1]
    letterDict = dict(sorted(letterDict.items(), key=lambda item: item[1]))
    # print(letterDict)
    return letterDict

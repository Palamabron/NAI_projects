import random
import string
import numpy as np
from os import walk


def filteredFilesToList(directory='data'):
    languageLabels, languageData, trainData = [], [], []
    for (_, dirnames, _) in walk(directory):
        if len(languageLabels) == 0:
            languageLabels = dirnames
        for subdirectory in dirnames:
            subpath = directory + '/' + subdirectory
            for (_, _, filenames) in walk(subpath):
                for filename in filenames:
                    filepath = directory + '/' + subdirectory + '/' + filename
                    with open(filepath, 'r', encoding='utf-8') as file:
                        fileContent = file.read()
                        fileContent = fileContent.lower()
                        for char in set(fileContent):
                            if char not in list(string.ascii_lowercase):
                                fileContent = fileContent.replace(char, '')
                        languageData.append(fileContent)
            trainData.append(languageData)
            languageData = []
    return trainData, languageLabels


def testDataToNormVector(text):
    text = text.lower()
    tmp = set(text)
    for char in tmp:
        if char in list(string.punctuation):
            text = text.replace(char, '')
        elif char in list(string.whitespace):
            text = text.replace(char, '')
        elif char not in list(string.ascii_lowercase):
            text = text.replace(char, '')
    letterCountList = [0] * 26
    freqList = [0.0] * 26
    alphabetList = list(string.ascii_lowercase)
    for i in range(len(alphabetList)):
        letterCountList[i] = text.count(alphabetList[i])
    for i in range(len(alphabetList)):
        freqList[i] = (letterCountList[i] / sum(letterCountList)) * 100

    return freqList


def countLetters(trainingData):
    letterCountList = []
    for i in range(len(trainingData)):
        tmp = []
        for _ in trainingData[i]:
            tmp.append(np.zeros(26, dtype=int))
        letterCountList.append(tmp)
    alphabetList = list(string.ascii_lowercase)
    for i in range(len(trainingData)):
        for j in range(len(trainingData[i])):
            for letter in alphabetList:
                letterCountList[i][j][alphabetList.index(letter)] += trainingData[i][j].count(letter)
    return np.array(letterCountList, dtype=object)


def normalizeVector(letterCountList):
    freqList = []
    for i in range(len(letterCountList)):
        language = []
        for j in range(len(letterCountList[i])):
            freqs = []
            for k in range(len(letterCountList[i][j])):
                freqs.append(0.0)
            language.append(freqs)
        freqList.append(language)
    for i in range(len(letterCountList)):
        for j in range(len(letterCountList[i])):
            suma = 0.0
            for k in range(len(letterCountList[i][j])):
                suma += letterCountList[i][j][k] ** 2
            suma = np.sqrt(suma)
            for k in range(len(letterCountList[i][j])):
                tmp = letterCountList[i][j][k]
                result = tmp / suma
                freqList[i][j][k] = result
    return freqList

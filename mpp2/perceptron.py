import random
import matplotlib.pyplot as plt
import numpy as np


class Perceptron:
    def __init__(self, train_list, test_list, learning_const):
        self.trainList = train_list
        self.testList = test_list
        self.learningConst = learning_const
        self.weights = list(np.random.random_sample(getAttribNumber(train_list)))
        self.threshold = len(self.weights) * 2.0
        self.weights.append(self.threshold)
        self.weightsHistory = [self.weights]

    def deltaEvaluation(self):
        random.shuffle(self.trainList)
        # print(f"weights: {self.weights}")
        labelIndex = getLabelIndex(self.trainList)
        labels = getLabelDict(self.trainList)
        values = getValues(self.trainList)
        i = 0
        secondTry = False
        while i < len(values):
            net = 0.0
            multiplier = 0
            for j in range(len(values[i])):
                net += values[i][j] * self.weights[j]
            decision = 1 if net >= 0 else 0
            # print(
            # f"Train{i+1}. Predicted: {list(labels.keys())[list(labels.values()).index(decision)]}, expected: {self.trainList[i][labelIndex]}")
            for label, value in labels.items():
                if self.trainList[i][labelIndex] == label:
                    multiplier = value - decision
                    if multiplier != 0:
                        for j in range(len(self.weights)):
                            self.weights[j] = round(self.weights[j] + multiplier * self.learningConst * values[i][j], 5)
                        self.weightsHistory.append(self.weights.copy())
                    break
                    # print(f"multi: {multiplier}")

            if multiplier == 0 or secondTry:
                i += 1
                secondTry = False
            else:
                secondTry = True
        print(f"weights: {self.weights}")
        self.threshold = self.weights[-1]

    def predict(self):
        values = getValues(self.testList)
        labelIndex = getLabelIndex(self.testList)
        labels = getLabelDict(self.trainList)
        accuracies = [0, 0]
        total = [0, 0]
        for i in range(len(values)):
            net = 0.0
            for j in range(len(values[i])):
                net += values[i][j] * self.weights[j]
            decision = 1 if net >= self.threshold else 0
            label = list(labels.keys())[decision]
            # print(f"{i}. Predicted label: {label}, Expected: {self.testList[i][labelIndex]}")
            if label == self.testList[i][labelIndex]:
                accuracies[labels.get(self.testList[i][labelIndex])] += 1
            total[labels.get(self.testList[i][labelIndex])] += 1
        for i in range(len(accuracies)):
            accuracies[i] = round((accuracies[i] / total[i]) * 100, 3)
            print(f"Accuracy for {list(labels.keys())[list(labels.values()).index(i)]}: {accuracies[i]}%")
        accuracy = round((accuracies[0] + accuracies[1]) / 2, 4)
        print(f"Total accuracy: {accuracy}%")
        if accuracy <= 80.0:
            self.deltaEvaluation()
            self.predict()

    def checkVector(self, vector):
        labels = getLabelDict(self.trainList)
        net = 0.0
        for j in range(len(vector)):
            net += vector[j] * self.weights[j]
        decision = 1 if net >= self.threshold else 0
        label = list(labels.keys())[decision]
        # print(f"{i}. Predicted label: {label}, Expected: {self.testList[i][labelIndex]}")
        return label
    
    def plotWeights(self):
        distinctColors = ['grey', 'olive', 'purple', 'green', 'brown', 'red', 'orange', 'blue']
        plotIndex = 0
        # print(self.weightsHistory)
        colors = random.sample(distinctColors, len(self.weightsHistory[0]))
        if len(self.weightsHistory)//10 == 0:
            self.deltaEvaluation()
        for i in range(0, len(self.weightsHistory), len(self.weightsHistory)//10):
            plt.figure(plotIndex).canvas.manager.set_window_title('Weights Comparison')
            for j in range(0, len(self.weightsHistory[i])):
                plt.scatter(j, self.weightsHistory[i][j], c=colors[j])
        legend = []
        for i in range(len(self.weightsHistory[0])-1):
            legend.append(f'weight {i+1}')
        legend.append('theta')
        plt.legend(legend, loc='upper left')
        plt.ylim(top=max(self.weights)*1.2)
        plt.show()


# item : value
# etykieta : wartosc
def getLabelDict(twoDList):
    labels = dict()
    labelValue = 0
    labelIndex = getLabelIndex(twoDList)
    for i in range(len(twoDList)):
        # print(twoDList[i][labelIndex])
        # print(labels.keys())
        if twoDList[i][labelIndex] not in labels.keys():
            labels[twoDList[i][labelIndex]] = labelValue
            labelValue += 1
        if len(labels) == 2:
            return labels
    return labels


def getAttribNumber(twoDList):
    attribs = 0
    for i in range(len(twoDList[0])):
        if isinstance(twoDList[0][i], float):
            attribs += 1
    return attribs


def getLabelIndex(twoDList):
    for i in range(len(twoDList[0])):
        if isinstance(twoDList[0][i], str):
            return i
    return len(twoDList[0]) - 1


def getValues(twoDList):
    values = []
    tmpRow = []
    for row in twoDList:
        for i in range(len(row)):
            if isinstance(row[i], float):
                tmpRow.append(row[i])
        tmpRow.append(-1.0)
        values.append(tmpRow)
        tmpRow = []
    return values


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


def main():
    with open('Data/iris_train.csv') as file:
        train_data = file.read()
    with open('Data/iris_test.csv') as file:
        test_data = file.read()
    trainList = fileToTwoDList(train_data, ',')
    testList = fileToTwoDList(test_data, ',')
    perceptron = Perceptron(trainList, testList, 0.2)
    perceptron.deltaEvaluation()
    print()
    perceptron.predict()
    perceptron.plotWeights()


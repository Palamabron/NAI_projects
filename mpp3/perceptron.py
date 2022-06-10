import random


class Perceptron:
    def __init__(self, labelIndex, learningRate, languagesList):
        self.labelIndex = labelIndex
        self.weights = []
        for _ in range(26):
            self.weights.append(random.random())
        self.theta = 2.9
        self.learning_rate = learningRate
        self.weights.append(self.theta)
        self.languagesList = languagesList
        self.acc = 0.0

    def deltaEvaluation(self, trainList):
        i, j = 0, 0
        secondTry = False
        acc, total = 0, 0
        while i < len(trainList):
            # print(f"weights: {self.weights}")
            while j < len(trainList[i]):
                net = 0.0
                for k in range(len(trainList[i][j])):
                    net += trainList[i][j][k] * self.weights[k]
                net -= self.weights[-1]
                decision = 1 if net >= 0 else 0
                expected = 1 if i == self.labelIndex else 0
                multiplier = expected - decision

                if multiplier != 0:
                    for k in range(len(self.weights) - 1):
                        self.weights[k] = self.weights[k] + multiplier * self.learning_rate * trainList[i][j][k]
                    self.weights[-1] = self.weights[-1] + -multiplier * self.learning_rate
                    self.theta = self.weights[-1]
                if multiplier == 0 or secondTry:
                    if multiplier == 0:
                        acc += 1
                    total += 1
                    j += 1
                    secondTry = False
                else:
                    secondTry = True
            self.theta = self.weights[-1]
            i += 1
            j = 0
        self.acc = acc / total
        # print(f'accuracy: {accuracy}')

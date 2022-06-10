import math
import random

from perceptron import Perceptron
from dataManipulation import testDataToNormVector


class NeuronLayer:
    def __init__(self, trainSet, languagesSet, learningRate):
        self.trainList = trainSet
        self.languagesList = languagesSet
        self.learningRate = learningRate
        self.perceptrons = []
        for i in range(len(trainSet)):
            self.perceptrons.append(Perceptron(i, learningRate, languagesSet))

    def __str__(self):
        result = ""
        for perceptron in self.perceptrons:
            result += f"{self.languagesList[perceptron.labelIndex]} weights: {perceptron.weights}\n"
        return result

    def normalizePerceptronsWeights(self):
        for i in range(len(self.perceptrons)):
            weightsSum = sum(self.perceptrons[i].weights, -self.perceptrons[i].theta)
            for j in range(len(self.perceptrons[i].weights) - 1):
                self.perceptrons[i].weights[j] /= weightsSum

    def trainWeights(self, times=1):
        for _ in range(times):
            for i in range(len(self.perceptrons)):
                [random.shuffle(sublist) for sublist in self.trainList]
                tries = 0
                while self.perceptrons[i].acc < 0.8 or tries < 30:
                    self.perceptrons[i].deltaEvaluation(self.trainList)
                    tries += 1
        self.normalizePerceptronsWeights()

    def checkTextLanguage(self, text):
        letterProportionList = testDataToNormVector(text)
        languages = self.languagesList.copy()
        sigValues = []
        nets = []
        for perceptron in self.perceptrons:
            net = 0.0
            for i in range(len(perceptron.weights) - 1):
                net += perceptron.weights[i] * letterProportionList[i]
            net -= perceptron.weights[-1]
            nets.append(net)
        # minimum = abs(min(nets)) / 2
        for i in range(len(nets)):
            # nets[i] += minimum
            sigValues.append(1 / (1 + math.exp(-nets[i])))
        # predictionIndex = sigValues.index(max(sigValues))
        # secondPrediction = nets.index(max(nets))

        sigValues, languages = zip(*sorted(zip(sigValues, languages)))
        result = f"{languages[-1]}\n\n\n"
        for i in reversed(range(len(sigValues))):
            result += f"{languages[i]}: {round(sigValues[i] * 100, 4)}\n"
        return result

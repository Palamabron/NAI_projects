import math
import random
from dataManipulation import getData


# vector: (weight, value, probability)
def calculate(data):
    capacity = data[0][0] + 60
    temperature = data[0][2] + 100
    permutations = dict()
    threshold = 0.1
    while len(permutations) == 0:
        vector = random.randint(1, sum([2 ** i for i in range(len(data[1]))]))
        vector = "{0:b}".format(vector)
        vector = list(vector)
        # print(vector)
        iteration = 0
        while temperature != 0 or len(permutations) != 0:
            iteration += 1
            permutations = dict()
            # permutations[''.join(vector)].update({(calcParam(vector, data[2]), calcParam(vector, data[1]))})
            vectorValue = calcParam(vector, data[1])
            permutations[''.join(vector)] = (calcParam(vector, data[2]), vectorValue, 0.0)
            # print(permutations)
            for i in range(len(list(permutations.keys())[0])):
                if not isinstance(vector, list):
                    vector = list(vector)
                tmpVector = vector[:]
                if tmpVector[i] == '0':
                    tmpVector[i] = '1'
                else:
                    tmpVector[i] = '0'
                tmpValue = calcParam(tmpVector, data[1])
                deltaValue = abs(vectorValue - tmpValue)
                permutations[''.join(tmpVector)] = (
                calcParam(tmpVector, data[2]), tmpValue, calcProbability(deltaValue, temperature))
            # print(permutations)
            copied_permutations = permutations.copy()
            for key in copied_permutations.keys():
                if permutations.get(key)[0] > capacity:
                    del permutations[key]
            permutations = sorted(permutations.items(), key=lambda x: x[1][2])
            if len(permutations) == 0:
                break
            vector = permutations[-1][0]
            print(f"{iteration}. New vector: {vector}, value: {permutations[-1][1][1]}, weight: {permutations[-1][1][0]}")
            temperature /= 2
            if temperature < threshold:
                print(f"Final Vector is: {vector}, value: {permutations[-1][1][1]}, weight: {permutations[-1][1][0]}")
                print(f"Maxweight: {capacity}")
                temperature = 0
                break


def calcProbability(deltaValue, temperature):
    tmp = deltaValue / temperature
    if tmp > 11:
        return 0
    return 1 / math.exp(tmp)


def calcParam(vector, dataVector):
    param = 0
    for i in range(len(vector)):
        if vector[i] == '1':
            param += dataVector[i]
    return param

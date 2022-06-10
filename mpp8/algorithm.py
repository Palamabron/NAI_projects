import math
import random
from dataManipulation import getData


# napisać do laski że temperatura nie bedzie wynosic 0 o chuj z tym %
# vector: (weight, value, probability)
def calculate(data):
    capacity = data[0][0] + 40
    temperature = data[0][2]
    permutations = dict()
    while len(permutations) == 0:
        vector = random.randint(1, sum([2 ** i for i in range(len(data[1]))]))
        vector = "{0:b}".format(vector)
        vector = list(vector)
        # print(vector)
        while temperature != 0 or len(permutations) != 0:
            permutations = dict()
            # permutations[''.join(vector)].update({(calcParam(vector, data[2]), calcParam(vector, data[1]))})
            vectorValue = calcParam(vector, data[1])
            permutations[''.join(vector)] = (calcParam(vector, data[2]), vectorValue, 0.0)
            # print(permutations)
            for i in range(len(list(permutations.keys())[0])):
                tmpVector = vector.copy()
                if tmpVector[i] == '0':
                    tmpVector[i] = '1'
                else:
                    tmpVector[i] = '0'
                tmpValue = calcParam(tmpVector, data[1])
                deltaValue = abs(vectorValue - tmpValue)
                permutations[''.join(tmpVector)] = (calcParam(tmpVector, data[2]), tmpValue, calcProbability(deltaValue, temperature))
            # print(permutations)
            copied_permutations = permutations.copy()
            for key in copied_permutations.keys():
                dupa = permutations.get(key)[0]
                if permutations.get(key)[0] > capacity:
                    del permutations[key]
            permutations = sorted(permutations.items(), key=lambda x: x[1][2])
            print(permutations)


def calcProbability(deltaValue, temperature):
    return math.exp(-deltaValue / temperature)


def calcParam(vector, dataVector):
    param = 0
    for i in range(len(vector)):
        if vector[i] == '1':
            param += dataVector[i]
    return param


calculate(getData())

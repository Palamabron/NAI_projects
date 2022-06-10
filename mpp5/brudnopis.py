from dataManipulation import *
from bayes import *

with open('Data/trainset.csv') as file:
    test_data = file.read()
test_list = fileToTwoDList(test_data)
test_values = getValuesSet(test_list)
print(test_list)
print('##################')
print(test_values)
print(countPossibility(['slonecznie', 'tak', 'niska', 'srednia'], test_list))


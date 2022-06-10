import re

import PySimpleGUI as sg
from bayes import *
from dataManipulation import *


def createPathMenu():
    pathMenu = [
        [sg.Text('Please enter test dataset separator: '), sg.InputText(key='s1', size=2, enable_events=True)],
        [sg.Text('Please enter test dataset path: ')],
        [sg.InputText(key='p1')],
        [sg.Text('Please enter train dataset separator: '), sg.InputText(key='s2', size=2, enable_events=True)],
        [sg.Text('Please enter train dataset path: ')],
        [sg.InputText(key='p2')],
        [sg.Text('Please enter alpha const (for laplace smoothing): '),
         sg.InputText(key='alpha', size=2, enable_events=True)],
        [sg.Button('Exit', size=8), sg.Push(), sg.Button('Enter', key='pathEnter', size=8, disabled=True)],
        [sg.Text('', key='err')]
    ]
    return pathMenu


def createUserMenu():
    userMenu = [
        [sg.Button('Calculate labels for test dataset', size=25, key='test')],
        [sg.Button('Predict decision for input vector', size=25, key='vector')],
        [sg.Button('Exit', size=25)]
    ]
    return userMenu


def createVectorMenu(testList, labelsValues):
    inputTexts = [sg.InputText(key=str(f'in{i}'), enable_events=True, size=len(max(labelsValues[i], key=len))) for i in range(len(testList[0]))]
    options = [sg.Button('Exit', size=6), sg.Button('Back', key='backVMenu', size=6),
               sg.Button('Enter', key='enterVMenu', disabled=True, size=6)]
    vectorMenu = [
        [sg.Text('Enter vector:', justification='center')],
        [inputTexts],
        [sg.Text('Predicted label: ', key='pred1')],
        [options]
    ]
    return vectorMenu


def menu():
    sg.theme('Reds')

    window = sg.Window('Naive Bayes Classifier', createPathMenu())
    test_list, train_list = None, None
    labelsValues = None
    isPathMenu, isUserMenu, isVectorMenu = True, False, False
    alpha = 0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if isPathMenu:
            if len(values['p1']) > 0:
                if re.compile('[@_,!#$%^&*()<>?/|}{~:a-zA-Z]').search(values['alpha']) is None:
                    window['pathEnter'].update(disabled=False)
                    if event == 'pathEnter':
                        testPath = values['p1']
                        testPath = testPath.replace(" ", "").replace("\n", "").replace("\t", "")
                        testSep = values['s1']
                        trainPath = values['p2']
                        trainPath = trainPath.replace(" ", "").replace("\n", "").replace("\t", "")
                        trainSep = values['s2']

                        if values['alpha'] is None or values['alpha'] == '':
                            alpha = 1
                        else:
                            alpha = int(values['alpha'])
                        try:
                            with open(testPath) as file:
                                test_data = file.read()
                            with open(trainPath) as file:
                                train_data = file.read()
                            test_list = fileToTwoDList(test_data, testSep)
                            train_list = fileToTwoDList(train_data, trainSep)
                            labelsValues = getValuesSet(train_list)
                            # print(test_list)
                            window.close()
                            window = sg.Window('Menu', createUserMenu())
                            isPathMenu = False
                            isUserMenu = True
                            continue
                        except OSError:
                            window['err'].update('ERROR TRY AGAIN')
                        except Exception:
                            raise

        if isUserMenu:
            if event == 'test':
                testData(test_list, train_list)
            if event == 'vector':
                isUserMenu = False
                isVectorMenu = True
                window.close()
                window = sg.Window('Vector Input', createVectorMenu(test_list, labelsValues))
                continue

        if isVectorMenu:
            isFilled = True
            inputVector = []
            for i in range(len(train_list[0]) - 1):
                if len(values[f'in{i}']) == 0 or values[f'in{i}'] not in labelsValues[i]:
                    window['enterVMenu'].update(disabled=True)
                    isFilled = False
                    break

            if isFilled:
                window['enterVMenu'].update(disabled=False)

            if event == 'backVMenu':
                window.close()
                window = sg.Window('Menu', createUserMenu())
                isUserMenu = True
                isVectorMenu = False

            elif event == 'enterVMenu':
                for i in range(len(test_list[0])):
                    inputVector.append(values[f'in{i}'])
                calculatedPossibilities = countPossibility(inputVector, train_list, alpha)
                window['pred1'].update(f'Calculated possibilities for: \n{calculatedPossibilities}')
                for i in range(len(train_list[0]) - 1):
                    window[f'in{i}'].update('')
                window['enterVMenu'].update(disabled=True)


menu()

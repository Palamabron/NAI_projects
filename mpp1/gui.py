import re

import PySimpleGUI as sg
from knn import fileToTwoDList, plotList, checkVector, testEval, plotK


def createVectorMenu(dataList):
    inputTexts = [sg.InputText(key=str(f'in{i}'), enable_events=True, size=4) for i in range(len(dataList[0]) - 1)]
    options = [sg.Button('Exit', size=6), sg.Button('Back', key='backVMenu', size=6),
               sg.Button('Enter', key='enterVMenu', disabled=True, size=6)]
    vectorMenu = [
        [sg.Text('Enter vector:', justification='center')],
        [inputTexts],
        [sg.Text('Predicted label: ', key='pred1')],
        [options]
    ]
    return vectorMenu


def createPathMenu():
    pathMenu = [
        [sg.Text('Please enter train dataset separator: '), sg.InputText(key='s1', size=2)],
        [sg.Text('Please enter train dataset path: ')],
        [sg.InputText(key='p1')],
        [sg.Text('\n')],
        [sg.Text('Please enter test dataset separator: '), sg.InputText(key='s2', size=2)],
        [sg.Text('Please enter test dataset path: ')],
        [sg.InputText(key='p2')],
        [sg.Button('Exit', size=8), sg.Push(), sg.Button('Enter', key='pathEnter', size=8)],
        [sg.Text('', key='err')]
    ]
    return pathMenu


def createUserMenu():
    userMenu = [
        [sg.Button('Calculate label for vector', size=25, key='vector', disabled=True),
         sg.Text('Enter k: '), sg.InputText(key='kv', size=2, enable_events=True)],
        [sg.Button('Calculate labels for test dataset', size=25, key='test', disabled=True),
         sg.Text('Enter k: '), sg.InputText(key='kt', size=2, enable_events=True)],
        [sg.Button('Plot accuracy to k neighbors', key='plotK', size=25)],
        [sg.Button('Plot test dataset', key='plotTest', size=25)],
        [sg.Button('Plot train dataset', key='plotTrain', size=25)],
        [sg.Button('Exit', size=25)]
    ]
    return userMenu


def menu():
    sg.theme('DarkBlack1')

    window = sg.Window('KNN Calculator', createPathMenu())
    train_list, test_list = [], []
    isPathMenu, isUserMenu, isVectorMenu = True, False, False
    kv, kt = 1, 1
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if isPathMenu:
            if len(values['p1']) > 0 and len(values['p2']) > 0 and event == 'pathEnter':
                trainPath = values['p1']
                testPath = values['p2']
                trainPath = trainPath.replace(" ", "").replace("\n", "").replace("\t", "")
                testPath = testPath.replace(" ", "").replace("\n", "").replace("\t", "")
                trainSep = values['s1']
                testSep = values['s2']
                try:
                    with open(trainPath) as file:
                        train_data = file.read()
                    with open(testPath) as file:
                        test_data = file.read()
                    train_list, test_list = fileToTwoDList(train_data, trainSep), fileToTwoDList(test_data, testSep)
                    window.close()
                    window = sg.Window('Menu', createUserMenu())
                    isPathMenu = False
                    isUserMenu = True
                    continue
                except OSError:
                    window['err'].update('ERROR TRY AGAIN')
                except Exception as e:
                    raise

        if isUserMenu:
            if len(values['kv']) > 0 and values['kv'].isdigit():
                window['vector'].update(disabled=False)
                kv = int(values['kv'])

            if len(values['kt']) > 0 and values['kt'].isdigit():
                window['test'].update(disabled=False)
                kt = int(values['kt'])

            if event == 'vector':
                vectorMenu = createVectorMenu(train_list)
                window.close()
                window = sg.Window('Vector Menu', vectorMenu, element_justification='c')
                isUserMenu = False
                isVectorMenu = True
                continue

            if event == 'test':
                testEval(test_list, train_list, kt)

            if event == 'plotTest':
                plotList(test_list)

            if event == 'plotTrain':
                plotList(train_list)
            
            if event == 'plotK':
                plotK(test_list, train_list)

        if isVectorMenu:
            isFilled = True
            inputVector = [0.0] * (len(train_list[0]) - 1)
            for i in range(len(train_list[0]) - 1):
                if len(values[f'in{i}']) > 0:
                    if set(values[f'in{i}']).issubset(set('0123456789.')) and values[f'in{i}'].count(".") <= 1:
                        if '.' in values[f'in{i}'][1:] and values[f'in{i}'][-1].isdigit():
                            inputVector[i] = float(values[f'in{i}'])
                    elif re.compile('[@_!#$%^&*()<>?/|}{~:a-zA-Z]').search(values[f'in{i}']) is not None:
                        window.Element(f'in{i}').update('')
                    elif values[f'in{i}'].count(".") > 1:
                        window.Element(f'in{i}').update('')
                    else:
                        window.Element(f'in{i}').update(values[f'in{i}'][:-1])
                else:
                    isFilled = False

            if isFilled:
                window['enterVMenu'].update(disabled=False)

            if event == 'backVMenu':
                window.close()
                window = sg.Window('Menu', createUserMenu())
                isUserMenu = True
                isVectorMenu = False

            elif event == 'enterVMenu':
                predictedLabel = checkVector(inputVector, train_list, kv)
                window['pred1'].update(f'Predicted label: {predictedLabel}')
                for i in range(len(train_list[0]) - 1):
                    window[f'in{i}'].update('')
                window['enterVMenu'].update(disabled=True)


menu()

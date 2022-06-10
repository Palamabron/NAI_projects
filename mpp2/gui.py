import re
import PySimpleGUI as sg
from perceptron import fileToTwoDList, Perceptron


def createPathMenu():
    pathMenu = [
        [sg.Text('Please enter train dataset separator: '), sg.InputText(key='s1', size=2, enable_events=True)],
        [sg.Text('Please enter train dataset path: ')],
        [sg.InputText(key='p1')],
        [sg.Text('\n')],
        [sg.Text('Please enter test dataset separator: '), sg.InputText(key='s2', size=2, enable_events=True)],
        [sg.Text('Please enter test dataset path: ')],
        [sg.InputText(key='p2')],
        [sg.Text('Please enter learning constant: '), sg.InputText(key='a1', size=4, enable_events=True)],
        [sg.Button('Exit', size=8), sg.Push(), sg.Button('Enter', key='pathEnter', size=8, disabled=True)],
        [sg.Text('', key='err')]
    ]
    return pathMenu


def createUserMenu():
    userMenu = [
        [sg.Button('Calculate label for vector', size=25, key='vector')],
        [sg.Button('Calculate labels for test dataset', size=25, key='test')],
        [sg.Button('Plot weights', size=25, key='plot')],
        [sg.Button('Exit', size=25)]
    ]
    return userMenu


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


def menu():
    sg.theme('Reds')

    window = sg.Window('Perceptron', createPathMenu())
    train_list, test_list = [], []
    isPathMenu, isUserMenu, isVectorMenu = True, False, False
    perceptron = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if isPathMenu:
            if len(values['a1']) == 3 and '.' in values['a1'] and values['a1'][2] != '0':
                values['a1'] += '0'
                window['a1'].update(values['a1'])
            if len(values['p1']) > 0 and len(values['p2']) > 0 and len(values['a1']) > 0:
                if re.compile('[@_,!#$%^&*()<>?/|}{~:a-zA-Z]').search(values['a1']) is None:
                    window['pathEnter'].update(disabled=False)
                    if event == 'pathEnter':
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
                            # print(test_list)
                            window.close()
                            window = sg.Window('Menu', createUserMenu())
                            isPathMenu = False
                            isUserMenu = True
                            perceptron = Perceptron(train_list, test_list, float(values['a1']))
                            continue
                        except OSError:
                            window['err'].update('ERROR TRY AGAIN')
                        except Exception as e:
                            raise

        if isUserMenu:
            if event == 'test':
                perceptron.deltaEvaluation()
                perceptron.predict()

            if event == 'vector':
                vectorMenu = createVectorMenu(train_list)
                window.close()
                window = sg.Window('Vector Menu', vectorMenu, element_justification='c')
                isUserMenu = False
                isVectorMenu = True
                continue

            if event == 'plot':
                perceptron.plotWeights()

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
                predictedLabel = perceptron.checkVector(inputVector)
                window['pred1'].update(f'Predicted label: {predictedLabel}')
                for i in range(len(train_list[0]) - 1):
                    window[f'in{i}'].update('')
                window['enterVMenu'].update(disabled=True)


menu()

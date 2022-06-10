import re

import PySimpleGUI as sg
from dataManipulation import fileToTwoDList, deleteLabelFromData
from kMeans import plotDataPoints, calculateCentroids


def createPathMenu():
    pathMenu = [
        [sg.Text('Please enter train dataset separator: '), sg.InputText(key='s1', size=2, enable_events=True)],
        [sg.Text('Please enter train dataset path: ')],
        [sg.InputText(key='p1')],
        [sg.Text('Please enter number of clusters: '), sg.InputText(key='k1', size=2, enable_events=True)],
        [sg.Button('Exit', size=8), sg.Push(), sg.Button('Enter', key='pathEnter', size=8, disabled=True)],
        [sg.Text('', key='err')]
    ]
    return pathMenu


def createUserMenu():
    userMenu = [
        [sg.Button('Calculate labels for test dataset', size=25, key='test')],
        [sg.Button('Plot clusters', size=25, key='plot', disabled=True)],
        [sg.Button('Exit', size=25)]
    ]
    return userMenu


def menu():
    sg.theme('Reds')

    window = sg.Window('K-Means', createPathMenu())
    test_list = []
    isPathMenu, isUserMenu, isVectorMenu = True, False, False
    k1 = 0
    centroidAverages = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if isPathMenu:
            if len(values['p1']) > 0 and len(values['k1']) > 0:
                if re.compile('[@_,!#$%^&*()<>?/|}{~:a-zA-Z]').search(values['k1']) is None:
                    window['pathEnter'].update(disabled=False)
                    if event == 'pathEnter':
                        testPath = values['p1']
                        testPath = testPath.replace(" ", "").replace("\n", "").replace("\t", "")
                        testSep = values['s1']
                        k1 = int(values['k1'])
                        try:
                            with open(testPath) as file:
                                test_data = file.read()
                            test_list = fileToTwoDList(test_data, testSep)
                            test_list = deleteLabelFromData(test_list)
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
                centroidAverages, reClustered = calculateCentroids(test_list, k1)
                window['plot'].update(disabled=False)
            if event == 'plot':
                plotDataPoints(reClustered, centroidAverages)


menu()

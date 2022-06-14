import PySimpleGUI as sg
from huffman import calculate
from dataManipulation import getData
from os.path import exists


def createPathMenu():
    pathMenu = [
        [sg.Text('Please enter test dataset path: ')],
        [sg.InputText(key='p1')],
        [sg.Button('Exit', size=8), sg.Push(), sg.Button('Enter', key='pathEnter', size=8)],
        [sg.Text('', key='err')]
    ]
    return pathMenu


def createUserMenu():
    userMenu = [
        [sg.Button('Brute Force', size=25, key='bruteForce')],
        [sg.Button('Exit', size=25)]
    ]
    return userMenu


def menu():
    sg.theme('Reds')

    window = sg.Window('Hill climbing', createPathMenu())
    isPathMenu, isUserMenu, isVectorMenu = True, False, False
    data = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if isPathMenu:
            if event == 'pathEnter':
                dataPath = values['p1']
                dataPath = dataPath.replace(" ", "").replace("\n", "").replace("\t", "")
                if dataPath is None or dataPath == "":
                    data = getData()
                else:
                    if exists(dataPath):
                        data = getData(path=dataPath)
                    else:
                        window['err'].update("File in given path doesn't exists!")
                        continue
                window.close()
                window = sg.Window('Menu', createUserMenu())
                isPathMenu = False
                isUserMenu = True
                continue

        if isUserMenu:
            if event == 'bruteForce':
                calculate(data)


menu()

import PySimpleGUI as sg
from dataManipulation import filteredFilesToList, countLetters, normalizeVector
import neuronLayer


def createPathMenu():
    pathMenu = [
        [sg.Text('Please enter train dataset directory path: ', justification='center', size=40)],
        [sg.InputText(key='dirPath')],
        [sg.Text('Please enter learning constant: '), sg.Push(), sg.InputText(key='const', size=4, enable_events=True)],
        [sg.Button('Exit', size=8), sg.Push(), sg.Button('Enter', key='pathEnter', size=8, disabled=True)],
        [sg.Text('', key='err')]
    ]
    return pathMenu


def createUserMenu():
    userMenu = [
        [sg.Text('Enter text that you want to check:', justification='center', size=60)],
        [sg.Multiline(key='testText', size=(60, 40))],
        [sg.Text('Prediction:', key='prediction')],
        [sg.Button('Exit', size=25), sg.Button('Enter', size=25)]
    ]
    return userMenu


def menu():
    sg.theme('DarkBlack1')

    window = sg.Window('Neuron Layer', createPathMenu())
    trainList, languagesList = [], []
    layer = None
    isPathMenu, isUserMenu, isVectorMenu = True, False, False
    isFirstEnter = True
    const = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if isPathMenu:
            # dodać learning const
            if len(values['const']) > 0:
                if set(values['const']).issubset(set('0123456789.')) and values['const'].count(".") == 1:
                    if values['const'][-1].isdigit():
                        window['pathEnter'].update(disabled=False)
            if event == 'pathEnter':
                if len(values['dirPath']) > 0:
                    trainPath = values['dirPath']
                    trainPath = trainPath.replace(" ", "").replace("\n", "").replace("\t", "")
                    try:
                        trainList, languagesList = filteredFilesToList(directory=trainPath)
                    except OSError:
                        window['err'].update('ERROR TRY AGAIN')
                    except Exception:
                        raise
                else:
                    try:
                        trainList, languagesList = filteredFilesToList()
                    except OSError:
                        window['err'].update('ERROR TRY AGAIN')
                    except Exception:
                        raise
                const = values['const']
                trainList = normalizeVector(countLetters(trainList))
                layer = neuronLayer.NeuronLayer(trainList, languagesList, float(const))
                layer.trainWeights()
                print(str(layer))
                window.close()
                window = sg.Window('Menu', createUserMenu())
                isPathMenu = False
                isUserMenu = True
                continue

        if isUserMenu:
            if event == 'Enter' and len(values['testText']) > 0:
                text = values['testText']
                if isFirstEnter:
                    prediction = layer.checkTextLanguage(text)
                    window['prediction'].update(f'Prediction: {prediction}')
                    isFirstEnter = False
                else:
                    layer = neuronLayer.NeuronLayer(trainList, languagesList, float(const))
                    layer.trainWeights()
                    print(str(layer))
                    prediction = layer.checkTextLanguage(text)
                    window['prediction'].update(f'Prediction: {prediction}')


menu()

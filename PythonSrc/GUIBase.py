import PySimpleGUI as sg
import threading

class Middlebox_GUI:
    def DefaultFunction(Argu):
        print("Emergency")


    Title = 'Middlebox'
    Camera1='Camera 1'
    Camera2='Camera 2'
    EmergencyFunction1=DefaultFunction
    EmergencyFunction2=DefaultFunction
    def __init__(self,GivenTitle,Text1,Text2,EmergencyFunc1,EmergencyFunc2):
        self.Title = GivenTitle
        self.Camera1=Text1
        self.Camera2=Text2
        self.EmergencyFunction1=EmergencyFunc1
        self.EmergencyFunction2=EmergencyFunc2
        

    
    def RunGUI(self):
        LeftColumn = [
        [sg.Text(self.Camera1)],
        [sg.Button(self.Camera1), sg.Button('Not Emergency 1')]

        ]
        RightColumn = [
        [sg.Text(self.Camera2)],
        [sg.Button(self.Camera2), sg.Button('Not Emergency 2')]
        ]
        Exit = [
        [sg.Button('Exit')]
        ]

        window=sg.Window(title=self.Title, layout=[LeftColumn,RightColumn,Exit], margins=(144,144))
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == self.Camera1:
                self.EmergencyFunction1(self.Camera1)
            if event == self.Camera2:
                self.EmergencyFunction2(self.Camera2)
            if event == 'Not Emergency 1' or event == 'Not Emergency 2':
                print("No Emergency")


        window.close()
class EmergencyCenterGUI:
    def defaultfunction(args):
        print()
    Title = 'Emergency Center'
    Middlebox1 = 'Middlebox 1'
    Middlebox2 = 'Middlebox 2'
    Camera1='Camera 1'
    Camera2='Camera 2'
    Camera3='Camera 3'
    Camera4='Camera 4'
    EmergencyString1='Emergency 1'
    EmergencyString2='Emergency 2'
    EmergencyString3='Emergency 3'
    EmergencyString4='Emergency 4'

    EmergencyResponseFunction=defaultfunction
    NonemergencyResponseFunction=defaultfunction

    def __init__(self,EmergencyFunction,NonEmergencyFunction):
        self.EmergencyResponseFunction=EmergencyFunction
        self.NonemergencyResponseFunction=NonEmergencyFunction

        pass
    def RunGUI(self):
        FirstCamera = [
        [sg.Text(self.Camera1)],
        [sg.Button(self.EmergencyString1), sg.Button('Not Emergency 1')]

        ]
        SecondCamera = [
        [sg.Text(self.Camera2)],
        [sg.Button(self.EmergencyString2), sg.Button('Not Emergency 2')]
        ]
        ThirdCamera = [
        [sg.Text(self.Camera3)],
        [sg.Button(self.EmergencyString3), sg.Button('Not Emergency 3')]

        ]
        FourthCamera = [
        [sg.Text(self.Camera4)],
        [sg.Button(self.EmergencyString4), sg.Button('Not Emergency 4')]
        ]
        Exit = [
        [sg.Button('Exit')]
        ]

        window=sg.Window(title=self.Title, layout=[FirstCamera,SecondCamera,ThirdCamera,FourthCamera,Exit], margins=(144,144))
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == self.EmergencyString1:
                self.EmergencyResponseFunction(self.EmergencyString1)
            if event == self.EmergencyString2:
                self.EmergencyResponseFunction(self.EmergencyString2)
            if event == self.EmergencyString3:
                self.EmergencyResponseFunction(self.EmergencyString3)
            if event == self.EmergencyString4:
                self.EmergencyResponseFunction(self.EmergencyString4)    
            if event == 'Not Emergency 1' or event == 'Not Emergency 2':
                print("No Emergency")
                self.NonemergencyResponseFunction(self.EmergencyString1)
            if event == 'Not Emergency 3' or event == 'Not Emergency 4':
                print("No Emergency")
                self.NonemergencyResponseFunction(self.EmergencyString3)


        window.close()


class EmergencyGUI:
    def defaultfunction(args):
        print()


    Title = 'Emergency'
    Caller = 'Caller'
    EmergencyString = "Accept Emergency"
    NotEmergencyString = "Refuse Request"
    EmergencyResponseFunction=defaultfunction
    NonemergencyResponseFunction=defaultfunction

    def __init__(self,EmergencyFunction,NonEmergencyFunction,Title,Caller,EmergencyString):

        self.EmergencyResponseFunction=EmergencyFunction
        self.NonemergencyResponseFunction=NonEmergencyFunction
        self.Title=Title
        self.Caller=Caller
        self.EmergencyString=EmergencyString


    def RunGUI(self):
        MainText = [
        [sg.Text(self.Title), sg.Text("Called by: "+self.Caller)],
        [sg.Button(self.EmergencyString), sg.Button(self.NotEmergencyString)]
        ]
        Exit = [
        [sg.Button('Exit')]
        ]

        window=sg.Window(title=self.Title, layout=[MainText,Exit], margins = (80,80))
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == self.EmergencyString:
                self.EmergencyResponseFunction(self.EmergencyString)
                break
            if event == self.NotEmergencyString:
                self.NonemergencyResponseFunction(self.EmergencyString)
                break


        window.close()

#GUI=Middlebox_GUI('Middlebox 1','Camera1','Camera2')
#GUI.RunGUI()

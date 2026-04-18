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
        print(window)
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

#GUI=Middlebox_GUI('Middlebox 1','Camera1','Camera2')
#GUI.RunGUI()

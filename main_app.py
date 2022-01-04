import subprocess
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import P, SYSTEM_TRAY_MESSAGE_ICON_WARNING, Cancel, Col, Column, InputText, ScrolledTextBox, Window, change_look_and_feel, set_global_icon
from tkinter import *
import os 

class App:
    def __init__(self) -> None:
        self.layout = []
        self.column_to_right = []
        self.main_theme = sg.theme("LightGreen2")
        self.__window_to_show = None
    
    def main_window_settings(self):
        self.column_to_right = [
            [sg.Text('Доступные действия:')],
            [sg.Button('Сменить пароль пользователя')],
            [sg.Button("Папка TEMP")],
            [sg.Button("Открыть CMD")],
            [sg.HorizontalSeparator()],
            [sg.Text('Выберите путь скрипта')],
            [sg.InputText(key='scriptPath', readonly=True, background_color='black')],
            [sg.FileBrowse(target="scriptPath", key='-FILE_INNER-')],
            [sg.Button('Выполнить', enable_events=True), sg.Cancel('Сбросить')]
        ]
        self.layout = [
            [[sg.Text("Имя пользователя", pad=5, tooltip='Имя учетной записи'), sg.InputText()],
            [sg.Button(button_text='Забанить пользователя')],
            [sg.HorizontalSeparator()],
            [sg.Output(size=(40, 20), key="_output_"), sg.Column(self.column_to_right, vertical_alignment='right', justification='right'),],
            ]
        ]
        self.window1 = sg.Window('Delovoi Profil', icon='C://Users//Роман//Documents//Vadim//PythonFiles//app.ico').Layout(self.layout).Finalize()
        self.__window_to_show = self.window1
        return self.__window_to_show
    def event_loop(self, window_to_show):
        window_to_show()
        while True:
            window, event, values = sg.read_all_windows()
            # Проверка на нажатие крестика или наатие кнопки с надписью cancel
            if event in (None, 'Exit', 'Cancel'):
                break
                exit(0)
            
            if event == "Забанить пользователя":
                try:
                    if values[0] == '' or "" or None:
                        self.window1.FindElement('_output_').Update('')
                        print('Забыли указать имя')
                    else: 
                        self.window1.FindElement('_output_').Update('')
                        os.system(f'start /wait cmd /c $name={values[0]} Set -ADAccountPassword $name -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "123098" -Force -Verbose) Disable-ADAccount $name -PassThru Remove-ADGroupMember -Identity !_Офис -Members $name Remove-ADGroupMember -Identity BitrixUser -Members $name Get-ADUser -Identity $name | Move-ADObject -TargetPath "OU=14day, DC=dp, DC=local"')
                        print(f'User has been banned')
                except Exception as e:
                    print(e)
            if event == "Открыть CMD":
                self.window1.FindElement('_output_').Update('')
                os.system("start /wait cmd")
                print('CMD открыта')
            
            if event == "Папка TEMP":
                self.window1.FindElement('_output_').Update('')
                os.system(f'start {os.path.realpath("C://Windows//Temp")}')
                print("Папка открыта")

            if event == "Выполнить" and values["-FILE_INNER-"]:
                self.window1.FindElement('_output_').Update('')
                if values["-FILE_INNER-"] != '':
                    script_path = values["-FILE_INNER-"]
                    self.read_script(script_path)
                    print('reading and running scripts')

                else:
                    self.window1.FindElement('_output_').Update('')
                    print("Укажите правильный путь")

            if event == "Сбросить":
                script_path = ''
                values['-FILE_INNER-'] = ''

                self.window1.FindElement("scriptPath").Update('')
                self.window1.FindElement('_output_').Update('')
                os.system("cmd /c cls")
            if event == "Сменить пароль пользователя":
                try:
                    self.event_loop(self.change_password_window())

                except Exception as e:
                    print(e)



    def change_password_window(self):
        layout=[
                [sg.Text('Введите имя пользователя')],
                [sg.InputText(key='UserName1')],
                [sg.Text('Введите новый пароль')],
                [sg.InputText(key='Password3', password_char='*')],
                [sg.Submit('Подтвердить')],
            ]
        self.window2 =  sg.Window('Change user password', layout, icon='C://Users//Роман//Documents//Vadim//PythonFiles//app.ico')
        
        
        return self.window2
    
    def read_script(self, script_path):
        try:
            # Выполнение скрипта с помощью powershell и библиотеки subprocess
            p = subprocess.Popen(['powershell.exe', script_path])
            p.communicate()
        except Exception as e:
            print(e)
        # Если пересанет работать выполнение скриптов, то раскоментировать код ниже и закоментировать 
        # код выше!!
        # with open(script_path) as file:
        #     for line in file:
        #         os.system(line)

    def run(self):
        self.event_loop(self.main_window_settings())




app = App()
app.run()

import subprocess
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import SYSTEM_TRAY_MESSAGE_ICON_WARNING, Cancel, Col, Column, InputText, ScrolledTextBox, Window, set_global_icon
from tkinter import *
import os 


sg.theme('DarkAmber')
column_to_be_righted = [
    [sg.Text('Доступные действия:')],
    [sg.Button('Сменить пароль пользователя')],
    [sg.Button("Папка TEMP")],
    [sg.Button("Открыть CMD")],
    [sg.HorizontalSeparator()],
    [sg.Text('Выберите путь скрипта')],
    [sg.InputText(key='scriptPath', readonly=True, background_color='black')],
    [sg.FileBrowse(target="scriptPath", key='-FILE_INNER-', file_types=("Text files", "*.txt"))],
    [sg.Button('Выполнить', enable_events=True), sg.Cancel('Сбросить')]
]
layout = [
    [[sg.Text("Имя пользователя", pad=5, tooltip='Имя учетной записи'), sg.InputText()],
    [sg.Button(button_text='Забанить пользователя')],
    [sg.HorizontalSeparator()],
    [sg.Output(size=(40, 20), key="_output_"), sg.Column(column_to_be_righted, vertical_alignment='right', justification='right'),],
    ]]


window1 = sg.Window('Delovoi Profil', icon='C://Users//Роман//Documents//Vadim//PythonFiles//app.ico').Layout(layout).Finalize()
while True:
    event, values = window1.read()
    if event == "Забанить пользователя":
        if values[0] == '' or "" or None:
            window1.FindElement('_output_').Update('')
            print('Забыли указать имя')
        else: 
            window1.FindElement('_output_').Update('')
            os.system(f'start /wait cmd /c $name={values[0]} Set -ADAccountPassword $name -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "123098" -Force -Verbose) Disable-ADAccount $name -PassThru Remove-ADGroupMember -Identity !_Офис -Members $name Remove-ADGroupMember -Identity BitrixUser -Members $name Get-ADUser -Identity $name | Move-ADObject -TargetPath "OU=14day, DC=dp, DC=local"')
            print(f'User has been banned')
    
    if event == "Сбросить":
        script_path = ''
        values['-FILE_INNER-'] = ''
        
        window1.FindElement("scriptPath").Update('')
        window1.FindElement('_output_').Update('')
        os.system("cmd /c cls")

    if event == "Выполнить" and values["-FILE_INNER-"]:
        window1.FindElement('_output_').Update('')
        if values["-FILE_INNER-"] != '':
            script_path = values["-FILE_INNER-"]
            def read_script():
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

            window1.FindElement('_output_').Update('')
            read_script()
            print('reading and running scripts')
        else:
            window1.FindElement('_output_').Update('')
            print("Укажите правильный путь")
    
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == "Папка TEMP":
        window1.FindElement('_output_').Update('')
        os.system(f'start {os.path.realpath("C://Windows//Temp")}')
        print("Папка открыта")
    if event == "Открыть CMD":
        window1.FindElement('_output_').Update('')
        os.system("start /wait cmd")
        print('CMD открыта')
    if event == "Сменить пароль пользователя":
        def make_win2():
            layout=[
                [sg.Text('Введите имя пользователя')],
                [sg.InputText(key='UserName1')],
                [sg.Text('Введите новый пароль')],
                [sg.InputText(key='Password3', password_char='*')],
                [sg.Submit('Подтвердить')],
            ]
            return sg.Window('Change user password', layout, icon='C://Users//Роман//Documents//Vadim//PythonFiles//app.ico')
        window  = make_win2()
        event, values = window.read()
    if event == "Подтвердить":
        try:
            lines = [f"Set-ADAccountPassword {values['UserName1']} -NewPassword {values['Password3']}"]
            for line in lines:
                p1 = subprocess.Popen([f'powershell.exe', f'{line}'])
                p1.communicate()
                window.close()
        except Exception as e:
            print(f"ex is {e}")      
            window.close()  

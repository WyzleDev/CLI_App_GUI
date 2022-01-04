import os
script_path = "C://Users//Роман//Desktop//script.ps1"
def read_script():
    try:
        with open(script_path) as file:
            for line in file:
                print(line)
                os.system(line)
    except Exception as e:
        print(e)
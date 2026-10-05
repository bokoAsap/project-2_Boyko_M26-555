import sys
import prompt

def welcome():
    print('Первая попытка запустить проект!')
    print('***\n<command> exit - выйти из программы\n<command> help - справочная информация')

    command = prompt.string('Введите команду: ') 

    if command == 'help':
        welcome()
    elif command == 'exit':
        sys.exit(0)
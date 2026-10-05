# Запуск, игровой цикл, парсинг команд
import shlex
import sys

import prompt

from . import core, utils


def welcome():
    print('Первая попытка запустить проект!')
    print('***\n<command> exit - выйти из программы')
    print('<command> help - справочная информация')

    command = prompt.string('Введите команду: ') 

    if command == 'help':
        welcome()
    elif command == 'exit':
        sys.exit(0)


def print_help():
    """
    Выводит сообщение help
    """
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def run():
    while True:
        current_metadata = utils.load_metadata('db_meta.json')
        print_help()

        user_input = prompt.string('Введите команду: ')

        args = shlex.split(user_input)
        command = args[0]

        match command:
            case "create_table":
                metadata = core.create_table(current_metadata, args[1], args[1:])
            case "list_tables":
                core.list_tables(current_metadata)
            case "drop_table":
                metadata = core.drop_table(current_metadata, args[1])
            case "help":
                print_help()
            case "exit":
                sys.exit(0) 
        utils.save_metadata('db_meta.json', metadata)    
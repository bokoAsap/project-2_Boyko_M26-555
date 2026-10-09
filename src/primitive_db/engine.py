# Запуск, игровой цикл, парсинг команд
import shlex

import prompt

from . import constants, core, parser, utils


def welcome():
    print('Первая попытка запустить проект!')
    print('***\n<command> exit - выйти из программы')
    print('<command> help - справочная информация')

    command = prompt.string('Введите команду: ') 

    if command == 'help':
        welcome()
    elif command == 'exit':
        return


def print_help():
    """
    Выводит сообщение help
    """
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print('\n***Операции с данными***')
    print("""<command> insert into <имя_таблицы> values 
        (<значение1>, <значение2>, ...)  - создать запись""")
    print("<command> select from <имя_таблицы> " \
    "where <столбец> = <значение> - прочитать записи по условию")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> " \
    "where <столбец_условия> = <значение_условия> - обновить запись")
    print("<command> delete from <имя_таблицы> " \
    "where <столбец> = <значение> - удалить запись")
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def run():
    print_help()
    while True:
        current_metadata = utils.load_metadata(constants.META_FILE)

        user_input = prompt.string('Введите команду: ')

        args = shlex.split(user_input)

        command = args[0]

        match command:
            case "create_table":
                current_metadata = core.create_table(current_metadata, 
                                                     args[1], args[2:])
            case "list_tables":
                core.list_tables(current_metadata)
            case "drop_table":
                current_metadata = core.drop_table(current_metadata, args[1])
            # insert into users values ("Sergei", 28, true)
            case "insert":
                table = core.insert(current_metadata, args[2], args[4:])

                if table is not None:
                    utils.save_table_data(args[2], table)
            # select from users where age = 28
            case "select":
                table = utils.load_table_data(args[2])

                if len(args) > 3:
                    where_clause = parser.parse_str_clause(args[3:])
                else:
                    where_clause = None

                core.select(table, where_clause)
            # update users set age = 29 where name = "Sergei"
            case "update":
                table = utils.load_table_data(args[1])

                set_clause = parser.parse_str_clause(args[2:6])
                where_clause = parser.parse_str_clause(args[6:])

                updated_table = core.update(table, set_clause, where_clause)

                if updated_table is not None:
                    utils.save_table_data(args[1], updated_table)
            case "delete":
                table = utils.load_table_data(args[2])

                where_clause = parser.parse_str_clause(args[3:])
                updated_table = core.delete(table, where_clause)

                if updated_table is not None:
                    utils.save_table_data(args[2], updated_table)
            case "info":
                table = utils.load_table_data(args[1])
                core.info(args[1], current_metadata, table)
            case "help":
                print_help()
            case "exit":
                return 
            case _:
                print('Неправильная команда')
        if current_metadata is not None:
            utils.save_metadata('db_meta.json', current_metadata)    
# основная логика работы с таблицами
from prettytable import PrettyTable

from . import decorators, utils


def id_add(columns: list) -> list:
    """
    Проверяет есть ли ID в списке столбцов
    Если есть в начале списка, то возвращает как есть
    Если есть, но форматирование изменено, то возвращает с правильным форматированием
    Если есть, но не в начале, то удаляет с текущей позиции и добавляет в начало
    Если нет, то добавляет в начало
    """
    id_index = None
    
    for i, column in enumerate(columns):
        if column.split(':')[0].lower() == 'id':
            id_index = i
            break

    if id_index is None:
        columns.insert(0, 'ID:int')
    
    elif id_index == 0:
        columns[0] = 'ID:int'
    else:
        columns.pop(id_index)
        columns.insert(0, 'ID:int')

    return columns


def name_check(metadata: dict, table_name: str) -> bool:
    """
    Проверяет наличие таблицы с таким именем в метаданных базы данных
    """
    return table_name in metadata


def types_check(columns: list) -> bool:
    """
    Проверяет корректность типов данных
    True выводит, если есть неподдерживаемый тип данных
    False, если типы данных корректны
    """
    for column in columns:
        if column.split(':')[-1] in ('int', 'str', 'bool'):
            continue
        else:
            return True
    return False


def validation(columns: dict, values: list) -> list:
    """
    Вытаскивает тип данных столбцов и 
    проверяет соответствуют ли передаваемые значения ему
    """
    punctuation = '",()'
    keys = list(columns.keys())
    for i in range(len(values)):
        for p in punctuation:
            if p in values[i]:
                values[i] = values[i].replace(p, '')
        if columns[keys[i+1]] == 'int':
            values[i] = int(values[i])
        elif columns[keys[i+1]] == 'bool':
            values[i] = values[i].lower() in ('true')
        
    return values


def make_table(table_data: list) -> PrettyTable:
    """
    Создает таблицу с помощью prettytable
    """
    table = PrettyTable()
    table.field_names = list(table_data[0].keys())
    table.add_rows([list(row.values()) for row in table_data])
    return table


def parse_clause(clause: dict) -> tuple:
    """
    Распаршивает условие
    """
    return tuple(clause.items())[0]

    
@decorators.handle_db_errors()
def create_table(metadata: dict, table_name: str, columns: list) -> dict:
    """
    Принимает текущие метаданные, имя таблицы и список столбцов.
    Автоматически добавляет столбец ID:int в начало списка столбцов
    Проверяет, не существует ли уже таблица с таким именем. Если да, выводить ошибку
    Проверяет корректность типов данных
    Если все проверки пройдены успешно обновляет словарь metadata и возвращает его
    """
    columns = id_add(columns)

    if name_check(metadata, table_name):
        raise KeyError(table_name)
    
    if types_check(columns):
        raise ValueError('Неподдерживаемый тип данных')

    metadata[table_name] = {
        'columns': dict(column.split(':', 1) for column in columns)
    }

    cols_str = ', '.join(columns)
    print(f"Таблица {table_name} успешно создана со столбцами: {cols_str}")
    return metadata
    

@decorators.handle_db_errors()
@decorators.confirm_action("удаление таблицы")
def drop_table(metadata: dict, table_name: str) -> dict:
    """
    Проверяет существование таблицы. Если таблицы нет, выводит ошибку
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    """
    if name_check(metadata, table_name):
        print(f'Таблица {table_name} успешно удалена.')
        metadata.pop(table_name)
    return metadata


@decorators.handle_db_errors()
def list_tables(metadata: dict) -> None:
    """
    Выводит все таблицы в базе данных
    """
    if not metadata:
        print('В базе данных пока нет таблиц')
    for tablename in metadata:
        print(f'- {tablename}\n')


@decorators.handle_db_errors()
@decorators.log_time
def insert(metadata: dict, table_name: str, values: list) -> list:
    """
    Проверяет, существует ли таблица
    Проверяет, что количество переданных значений соответствует количеству столбцов 
    (минус ID)
    Валидирует типы данных для каждого значения в соответствии со схемой в metadata
    Генерирует новый ID (например, max(IDs) + 1 или len(data) + 1)
    Добавляет новую запись (в виде словаря) в данные таблицы и возвращает их
    """
    if not name_check(metadata, table_name):
        raise KeyError(table_name)
    
    if len(values) != len(metadata[table_name]['columns']) - 1:
        raise ValueError(
            f'Ожидалось {len(metadata[table_name]["columns"]) - 1} значений, '
            f'получено {len(values)}'
        )
    
    validated_values = validation(metadata[table_name]['columns'], values)

    table = utils.load_table_data(table_name)

    new_id = max((row['ID'] for row in table), default=0) + 1
    full_values = [new_id] + validated_values

    keys = list(metadata[table_name]['columns'].keys())
    data = dict(zip(keys, full_values))

    table.append(data)
    print(f'Запись с ID={data["ID"]} успешно добавлена в таблицу {table_name}')
    return table


select_cache = decorators.create_cacher()

@decorators.handle_db_errors()
@decorators.log_time
def select(table_data: list, where_clause: dict = None) -> None:
    """
    Если where_clause не задан, возвращает все данные.
    Если задан, фильтрует и возвращает только подходящие записи.
    """
    if not table_data:
        raise KeyError()

    if where_clause is not None:
        column, cond = parse_clause(where_clause)

        if column not in table_data[0]:
            raise KeyError(column)

        key = (column, cond)

        def get_result():
            return [
                    row for row in table_data
                    if row[column] == int(cond)
                ]

        table_data = decorators.select_cache(key, get_result)
    

    table = make_table(table_data)
    
    print(table)


@decorators.handle_db_errors() 
def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    """
    Находит записи по where_clause.
    Обновляет в найденных записях поля согласно set_clause.
    Возвращает измененные данные.
    """
    if set_clause is None or where_clause is None:
        return table_data 

    where_column, where_cond = parse_clause(where_clause)
    set_column, set_value = parse_clause(set_clause)

    if where_column not in table_data[0]:
        raise KeyError(where_column)

    if set_column not in table_data[0]:
        raise KeyError(set_column)

    for row in table_data:
        if row[where_column] == where_cond:
            row[set_column] = set_value
            print(f'Запись с ID={row["ID"]} в таблице успешно обновлена')
        
    return table_data


@decorators.handle_db_errors()
@decorators.confirm_action("удаление записи")
def delete(table_data: list, where_clause: dict) -> list:
    """
    Находит записи по where_clause и удаляет их.
    Возвращает измененные данные.
    """
    where_column, where_cond = parse_clause(where_clause)
    
    if where_column not in table_data[0]:
        raise KeyError(where_column)

    table = []

    for row in table_data:
        if row[where_column] == where_cond:
            print(f'Запись с ID={row["ID"]} успешно удалена из таблицы')
        else:
            table.append(row)

    return table


@decorators.handle_db_errors()
def info(table_name: str, metadata: dict, table: list) -> None:
    """
    Выводит информацию о таблице
    Название, столбцы и количество записей
    """
    columns = [
        f'{col}:{col_type}' 
        for col, col_type in metadata[table_name]['columns'].items()
        ]

    print(f'Таблица: {table_name}')
    print(f'Столбцы: {', '.join(columns)}')
    print(f'Количество записей:{len(table)}')
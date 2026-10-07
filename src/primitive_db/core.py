# основная логика работы с таблицами
from prettytable import PrettyTable


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
    Вытаскивает тип данных столбцов и проверяет соответствуют ли передаваемые значения ему
    """
    keys = list(columns.keys())
    for i in range(len(values)):
        # if not value_type_check(values[i], columns[keys[i+1]]):
        #     print(f'Значение {values[i]} не соответсвует типу {columns[keys[i+1]]}')
        #     return False
        if columns[keys[i+1]] == 'int':
            values[i] = int(values[i])
        elif columns[keys[i+1]] == 'bool':
            values[i] = bool(values[i])
        
    return values


# def value_type_check(value: object, type: str) -> bool:
#     """
#     Проверяет соотвествует ли значение типу данных
#     """
#     return isinstance(value, type)


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
    column = clause.keys()[0]
    cond = clause.values()[0]
    return column, cond

    
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
        print(f'Ошибка: Таблица {table_name} уже существует')
        return metadata
    
    if types_check(columns):
        print('Ошибка: неподдерживаемый тип данных')
        return metadata

    metadata = {
        'columns': dict(column.split(':', 1) for column in columns),
        'data': []
    }

    cols_str = ', '.join(columns)
    print(f"Таблица {table_name} успешно создана со столбцами: {cols_str}")
    return metadata
    

def drop_table(metadata: dict, table_name: str) -> dict:
    """
    Проверяет существование таблицы. Если таблицы нет, выводит ошибку
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    """
    if name_check(metadata, table_name):
        print(f'Таблица {table_name} успешно удалена.')
        metadata.pop(table_name)
    else:
        print(f'Ошибка: Таблица {table_name} не существует.')
    return metadata


def list_tables(metadata: dict) -> None:
    """
    Выводит все таблицы в базе данных
    """
    if not metadata:
        print('Ошибка: В базе данных пока нет таблиц')
    for tablename in metadata:
        print(f'- {tablename}\n')


def insert(metadata: dict, table_name: str, values: list) -> dict:
    """
    Проверяет, существует ли таблица
    Проверяет, что количество переданных значений соответствует количеству столбцов (минус ID)
    Валидирует типы данных для каждого значения в соответствии со схемой в metadata
    Генерирует новый ID (например, max(IDs) + 1 или len(data) + 1)
    Добавляет новую запись (в виде словаря) в данные таблицы и возвращает их
    """
    if not name_check(metadata, table_name):
        print(f'Ошибка: Таблица {table_name} не существует')
        return metadata
    
    if len(values) != len(metadata['columns']) - 1:
        print(f'Ошибка: Количество переданных значений не соответсвует количеству столбцов таблицы {table_name}')
        return metadata
    
    validated_values = validation(metadata['columns'], values)

    new_id = len(metadata['data'])
    full_values = [new_id] + validated_values

    keys = list(metadata['columns'].keys())
    data = dict(zip(keys, full_values))

    metadata['data'].append(data)
    return metadata


def select(table_data: list, where_clause: dict = None) -> None:
    """
    Если where_clause не задан, возвращает все данные.
    Если задан, фильтрует и возвращает только подходящие записи.
    """
    table = make_table(table_data)

    if where_clause is not None:
        column, cond = parse_clause(where_clause)
        print(table.get_string(row_filter=lambda row: row[column] == int(cond)))
        return
    
    print(table)


def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    """
    Находит записи по where_clause.
    Обновляет в найденных записях поля согласно set_clause.
    Возвращает измененные данные.
    """
    if set_clause is None or where_clause is None:
        print(f'Ошибка: Неполное условие')
        return table_data 

    where_column, where_cond = parse_clause(where_clause)
    set_column, set_value = parse_clause(set_clause)

    for row in table_data:
        if row[where_column] == where_cond:
            row[set_column] = set_value
    return table_data


def delete(table_data: list, where_clause: dict) -> list:
    """
    
    """
    if where_clause is None:
        print(f'Ошибка: Неполное условие')
        return table_data 
    
    where_column, where_cond = parse_clause(where_clause)

    for row in table_data[:]:
        if row[where_column] == where_cond:
            table_data.remove(row)
    return table_data
    
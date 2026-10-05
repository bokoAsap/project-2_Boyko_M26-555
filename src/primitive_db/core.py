# основная логика работы с таблицами
def id_add(columns: list) -> list:
    """
    Проверяет есть ли ID в списке столбцов
    Если есть в начале списка, то возвращает как есть
    Если есть, но форматирование изменено, то возвращает с правильным форматированием
    Если есть, но не в начале, то удаляет с текущей позиции и добавляет в начало
    Если нет, то добавляет в начало
    """
    if columns[0]['name'] == 'ID':
        return columns
    
    id_index = 1000
    for i, column in enumerate(columns):
        if column['name'] in ('ID', 'id', 'Id'):
            id_index = i
            break
    if id_index == 1000:
        return columns.insert(0, 
                                {
                                'name': 'ID',
                                'type': 'int'
                                }
                              )
    elif id_index == 0:
        return columns[id_index]['name'].upper()
    else:
        columns = columns.pop(id_index)
        return columns.insert(0, 
                                {
                                'name': 'ID',
                                'type': 'int'
                                }
                            )


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
        if column['type'] in ('int', 'str', 'bool'):
            continue
        else:
            return True
    return False

    
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
    
    if types_check(columns):
        print('Ошибка: неподдерживаемый тип данных')

    metadata[table_name] = columns

    cols_str = ', '.join(f"{col['name']}: {col['type']}" for col in columns)
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

def list_tables(metadata: dict) -> None:
    """
    Выводит все таблицы в базе данных
    """
    for tablename in metadata:
        print(f'- {tablename}\n')
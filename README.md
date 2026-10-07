# project-2_Boyko_M26-555
## Управление таблицами
После запуска database открывается интерактивный режим. Команды вводятся в одной строке, аргументы разделяются пробелами (разбор — через shlex.split, поэтому кавычки работают).

### Доступные команды
| Команда |	Синтаксис |	Описание |
| ------- | --------- | ---------|
| help | help |	Показать справку по командам |
| exit | exit |	Выйти из программы |
| create_table | create_table <имя> <колонка>:<тип> ... | Создать новую таблицу |
| drop_table | drop_table <имя> | Удалить таблицу |
| list_tables |	list_tables | Показать список всех таблиц |

### Типы данных
При создании таблицы поддерживаются три типа столбцов:\
- int — целое число;
- str — строка;
- bool — логическое значение.\
Столбец ID:int добавляется в начало автоматически — указывать его вручную не нужно.

### Пример использования
> database

<command> create_table <name> <column>:<type> ... - создать таблицу
<command> drop_table <name> - удалить таблицу
<command> list_tables - показать все таблицы
<command> help - справочная информация
<command> exit - выйти из программы

Введите команду: create_table users name:str age:int is_active:bool
Таблица 'users' создана.

Введите команду: create_table orders user_id:int total:int
Таблица 'orders' создана.

Введите команду: list_tables
users
orders

Введите команду: drop_table orders
Таблица 'orders' удалена.

Введите команду: list_tables
users

Введите команду: exit

### Ошибки
Команда сообщит об ошибке, если:\
- таблица с таким именем уже существует (create_table);
- указанного типа нет среди int/str/bool (create_table);
- таблицы с таким именем нет (drop_table);
- команда или аргументы введены неверно. \
Метаданные сохраняются в JSON-файл после каждой успешной операции create_table и drop_table, поэтому состояние таблиц переживает перезапуск программы.

## CRUD-операции
Реализованы основные CRUD-команды для работы с таблицами.

### INSERT
Добавляет новую запись в таблицу.
Команда:
```
insert into <table_name> values (<value1>, <value2>, ...)
```
При добавлении записи:
- проверяется существование таблицы;
- проверяется количество переданных значений;
- проверяются типы данных согласно `metadata`;
- автоматически генерируется новый `ID`.
Пример:
```
insert into users values ("Sergei", 25)
```
### SELECT
Выводит данные из таблицы.
Все записи:
```
select from users
```
С фильтрацией:

```
select from users where age = 25
```
Если WHERE не указан, выводятся все записи. Если условие задано — только подходящие.
### UPDATE
Изменяет существующие записи.
Синтаксис:
```
update <table_name> set <column> = <value> where <column> = <value>
```
Пример:
```
update users set age = 26 where name = "Sergei"
```
Команда находит записи по условию WHERE и изменяет указанные в SET поля.
### DELETE
Удаляет записи из таблицы.
Синтаксис:
```
delete from <table_name> where <column> = <value>
```
Пример:
```
delete from users where name = "Sergei"
```
Удаляются все записи, соответствующие условию WHERE.
### INFO
Выводит информацию о таблице:
- название таблицы;
- список столбцов;
- количество записей.
Пример:
```
info users
```
Пример результата:
```
Таблица: users
Столбцы: ID:int, name:str, age:int
Количество записей: 5
```

### Asciinema-demo
[![asciicast](https://asciinema.org/a/4wEeKPU8DIUdHJxC.svg)](https://asciinema.org/a/4wEeKPU8DIUdHJxC)
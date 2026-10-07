# Разбор сложных команд
def parse_str_clause(clause: list) -> dict:
    """
    Распаршивает условную часть запроса
    """
    without_keyword = ' '.join(clause[1:])
    key, value = without_keyword.split('=')

    return {key.strip(): value.strip()}
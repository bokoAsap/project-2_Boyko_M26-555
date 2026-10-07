# Разбор сложных команд
def parse_str_clause(clause: list) -> dict:
    """
    Распаршивает условную часть запроса
    """
    without_keyword = ' '.join(clause[1:])
    return dict(without_keyword.split('='))
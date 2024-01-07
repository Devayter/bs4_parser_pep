class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ParserFindPythonVertionsException(Exception):
    """Вызывается, если список версий отсутствует на странице."""
    pass


class SoupCreateException(Exception):
    """Вызывается при ошибке создания супа"""
    pass

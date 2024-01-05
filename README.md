# Парсер документации Python

## Обзор

Этот парсер документации Python разработан для извлечения информации с официального веб-сайта [Python](https://docs.python.org).

### Возможности

* whats_new: Парсинг раздела "Что нового в Python" для извлечения ссылок, заголовков и информации об редакторе/авторе.
* latest_versions: Извлечение информации о последних версиях Python, включая ссылки на документацию, номера версий и статус.
* download: Загрузка архива документации в формате PDF для формата A4.
* pep: Парсинг информации о предложениях по улучшению Python (PEP), включая статусы и количество.

### Использование

1. Клонирование репозитория:
`git clone https://github.com/Devayter/bs4_parser_pep`
`cd bs4_parser_pepr`
2. Установка зависимостей:
`pip install -r requirements.txt`
3. Запуск парсера:
`python main.py <mode> [-c] [-o <output>]`
Где mode - режим работы парсера, -c - очистка кэша, -o output - дополнительные параметры
вывода.
Для вызова описания парсера использовать команду:
`python main.py -h` или `python main.py --help`

## Режимы работы

1. whats-new - Парсинг нововведений в Python.
2. latest-versions - Информация о последних версиях Python.
3. download - Загрузка PDF-архива документации A4.
4. pep - Информация о предложениях по улучшению Python (PEP).
Вывод данных

### Парсер поддерживает два типа вывода

1. pretty - Красивый вывод в консоль с использованием PrettyTable.
2. file - Сохранение результатов в CSV-файл в директории results.

## Примеры использования

Парсинг нововведений в Python:
`python main.py whats-new`
Информация о последних версиях Python:
`python main.py latest-versions`
Загрузка PDF-архива документации A4:
`python main.py download`
Информация о предложениях по улучшению Python (PEP):
`python main.py pep`

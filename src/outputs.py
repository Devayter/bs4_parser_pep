import csv
import datetime as dt
import logging
import os

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, RESULTS_DIR


file_output_message = 'Файл с результатами был сохранён: {file_path}'


def control_output(results, cli_args):
    print(classmethod)
    output = cli_args.output
    if output in OUTPUTS:
        OUTPUTS[output](results, cli_args)
    else:
        default_output(results)


def default_output(results):
    print(results)
    for row in results:
        print(*row)


def pretty_output(*args):
    results = args[0]
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args, encoding='utf-8'):
    if os.environ.get('TEST_MODE'):
        results_dir = BASE_DIR / 'results'
    else:
        results_dir = RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding=encoding) as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(file_output_message.format(file_path=file_path))


OUTPUTS = {
    'pretty': pretty_output,
    'file': file_output
}

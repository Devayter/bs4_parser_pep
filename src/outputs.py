import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (BASE_DIR, DATETIME_FORMAT, DEFAULT, OUTPUT_FILE,
                       OUTPUT_PRETTY, RESULTS_FOLDER)


file_output_message = 'Файл с результатами был сохранён: {file_path}'


def control_output(results, cli_args, DEFAULT=DEFAULT):
    output = cli_args.output
    if output in OUTPUTS:
        OUTPUTS[output](results, cli_args)
    else:
        OUTPUTS[DEFAULT](results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args, encoding='utf-8'):
    results_dir = BASE_DIR / RESULTS_FOLDER
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
    OUTPUT_PRETTY: pretty_output,
    OUTPUT_FILE: file_output,
    DEFAULT: default_output
}

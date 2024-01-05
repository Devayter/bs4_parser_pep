import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import DATETIME_FORMAT, RESULTS_DIR


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


def file_output(results, cli_args):
    RESULTS_DIR.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = RESULTS_DIR / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(file_output_message.format(file_path=file_path))


OUTPUTS = {
    'pretty': pretty_output,
    'file': file_output
}

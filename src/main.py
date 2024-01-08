import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS_FOLDER, EXPECTED_STATUS,
                       MAIN_DOC_URL, PEP_DOC_URL)
from exceptions import (ParserFindPythonVertionsException,
                        ParserFindTagException)
from outputs import control_output
from utils import find_tag, find_tags_by_selector, get_soup

COMMAND_LINES_ARGUMENTS_MESSAGE = 'Аргументы командной строки: {args}'
DOWNLOAD_COMPLETE_MESSAGE = 'Архив был загружен и сохранён: {archive_path}'
DOWNLOAD_ERROR_MESSAGE = 'Некорректная ссылка для скачивания документации'
EXCEPT_ERROR_MESSAGE = 'Сбой в работе парсера {error}'
LOGS_MESSAGE = ('Несовпадающие статусы: '
                '{detail_link} '
                'Статус в карточке: {status_pep_detail_page} '
                'Ожидаемые статусы: {expected_status}')
NOTHING_WAS_FOUND_MESSAGE = 'Ничего не нашлось'
START_PARSER_MESSAGE = 'Парсер запущен!'
STOP_PARSER_MESSAGE = 'Парсер завершил работу'
SOUP_CREATE_ERROR = 'Ошибка при создании супа {error}'


def whats_new(session):
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    logs_messages = []
    for a_tag in tqdm(find_tags_by_selector(
        get_soup(session, urljoin(MAIN_DOC_URL, 'whatsnew/')),
        '#what-s-new-in-python div.toctree-wrapper:first-of-type '
        'a:contains("What")'
    )):
        href = a_tag['href']
        version_link = urljoin(urljoin(MAIN_DOC_URL, 'whatsnew/'), href)
        try:
            soup = get_soup(session, version_link)
            results.append(
                (version_link, find_tag(soup, 'h1').text,
                 find_tag(soup, 'dl').text.replace('\n', ' '))
            )
        except TypeError as error:
            logs_messages.append(
                SOUP_CREATE_ERROR.format(error=error)
            )
    list(map(logging.error, logs_messages))
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    ul_tags = find_tags_by_selector(soup, 'div.sphinxsidebarwrapper ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindPythonVertionsException(NOTHING_WAS_FOUND_MESSAGE)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    pdf_a4_link = soup.select_one(
        'div.body table.docutils a[href$="pdf-a4.zip"]'
        )['href']
    if not pdf_a4_link:
        raise ParserFindTagException(DOWNLOAD_ERROR_MESSAGE)
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_FOLDER
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_COMPLETE_MESSAGE.format(archive_path=archive_path))


def pep(session):
    statuses = defaultdict(int)
    soup = get_soup(session, PEP_DOC_URL)
    tr_tags = find_tags_by_selector(soup, 'section section#numerical-index tr')
    logs_info_messages, logs_error_messages = [], []
    for pep in tqdm(tr_tags[1:]):
        td_tags = pep.find_all('td')
        status = td_tags[0].text
        expected_status = EXPECTED_STATUS[status[1:]]
        href = find_tag(td_tags[1], 'a')['href']
        detail_link = urljoin(PEP_DOC_URL, href)
        try:
            soup = get_soup(session, detail_link)
            pep_info_section = find_tag(soup, 'section', {'id': 'pep-content'})
            status_pep_detail_page = find_tag(pep_info_section, 'abbr').text
            statuses[status_pep_detail_page] += 1
            if status_pep_detail_page not in expected_status:
                logs_info_messages.append(
                    LOGS_MESSAGE.format(
                        detail_link=detail_link,
                        status_pep_detail_page=status_pep_detail_page,
                        expected_status=expected_status
                    )
                )
        except TypeError as error:
            logs_error_messages.append(SOUP_CREATE_ERROR.format(error=error))
    list(map(logging.info, logs_info_messages))
    list(map(logging.error, logs_error_messages))
    return [
        ('Статус', 'Количество'),
        *statuses.items(),
        ('Всего', sum(statuses.values()))
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info(START_PARSER_MESSAGE)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(COMMAND_LINES_ARGUMENTS_MESSAGE.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results:
            control_output(results, args)
    except Exception as error:
        logging.error(
            EXCEPT_ERROR_MESSAGE.format(error=error),
            exc_info=True, stack_info=True
        )
    logging.info(STOP_PARSER_MESSAGE)


if __name__ == '__main__':
    main()

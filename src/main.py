import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (DOWNLOADS_DIR, EXPECTED_STATUS, MAIN_DOC_URL,
                       PEP_DOC_URL)
from exceptions import (ParserFindPythonVertionsException,
                        ParserFindTagException)
from outputs import control_output
from utils import (find_tag, find_tags_by_selector, get_soup,
                   get_soup_for_iteration)


command_lines_arguments_message = 'Аргументы командной строки: {args}'
download_complete_message = 'Архив был загружен и сохранён: {archive_path}'
download_error_message = 'Некорректная ссылка для скачивания документации'
start_parser_message = 'Парсер запущен!'
stop_parser_message = 'Парсер завершил работу'


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    sections_by_python = find_tags_by_selector(
        soup,
        '#what-s-new-in-python div.toctree-wrapper:first-of-type li.toctree-l1'
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_soup_for_iteration(session, version_link)
        results.append(
            (version_link, find_tag(soup, 'h1').text,
             find_tag(soup, 'dl').text.replace('\n', ' '))
            )
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    ul_tags = find_tags_by_selector(soup, 'div.sphinxsidebarwrapper ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindPythonVertionsException('Ничего не нашлось')
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
        logging.error(download_error_message, stack_info=True)
        raise ParserFindTagException(download_error_message)
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(download_complete_message.format(archive_path=archive_path))


def pep(session):
    statuses = defaultdict(int)
    soup = get_soup(session, PEP_DOC_URL)
    result = [('Статус', 'Количество')]
    tr_tags = find_tags_by_selector(soup, 'section section#numerical-index tr')
    logs_messages = []
    for pep in tqdm(tr_tags[1:]):
        td_tags = pep.find_all('td')
        status = td_tags[0].text
        href = find_tag(td_tags[1], 'a')['href']
        detail_link = urljoin(PEP_DOC_URL, href)
        soup = get_soup_for_iteration(session, detail_link)
        pep_info_section = find_tag(soup, 'section', {'id': 'pep-content'})
        status_pep_detail_page = find_tag(pep_info_section, 'abbr').text
        statuses[status_pep_detail_page] += 1
        if status_pep_detail_page not in EXPECTED_STATUS[status[1:]]:
            logs_messages.append(
                f'Несовпадающие статусы: '
                f'{detail_link} '
                f'Статус в карточке: {status_pep_detail_page} '
                f'Ожидаемые статусы: {EXPECTED_STATUS[status[1:]]}'
            )
    logging.info(*logs_messages)
    for status, count in statuses.items():
        result.append((status, count))
    return [
        ('Статус', 'Количество'), *result, ('Всего', sum(statuses.values()))
        ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info(start_parser_message)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(command_lines_arguments_message.format(args=args))
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    try:
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.error(f'Сбой в работе парсера {error}', stack_info=True)
    logging.info(stop_parser_message)


if __name__ == '__main__':
    main()

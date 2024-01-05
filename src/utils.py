from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


response_url_error_message = 'Возникла ошибка при загрузке страницы {url}'
find_tag_error_message = 'Не найден тег {tag} {attrs}'
find_tags_selector_error_message = 'Некорректный тег в селекторе {selectors}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as exeption:
        raise exeption(response_url_error_message.format(url=url))


def get_soup(session, url):
    response = get_response(session, url)
    if response is None:
        return
    return BeautifulSoup(response.text, features='lxml')


def get_soup_for_iteration(session, url):
    response = get_response(session, url)
    if response is None:
        raise RequestException(response_url_error_message.format(url=url))
    return BeautifulSoup(response.text, features='lxml')


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=({} if attrs is None else attrs))
    if searched_tag is None:
        raise ParserFindTagException(
            find_tag_error_message.format(tag=tag, attrs=attrs)
            )
    return searched_tag


def find_tags_by_selector(soup, selectors):
    tag = soup.select(selectors)
    if not tag:
        raise ParserFindTagException(
            find_tags_selector_error_message.format(selectors=selectors)
            )
    return tag

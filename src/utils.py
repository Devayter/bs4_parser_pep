from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

RESPONSE_URL_ERROR = '{error} при загрузке страницы {url}'
FIND_TAG_ERROR = 'Не найден тег {tag} {attrs}'
FIND_TAGS_SELECTOR_ERROR = 'Не найден тег в селекторе {selectors}'


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ConnectionError(
            RESPONSE_URL_ERROR.format(url=url, error=error)
            )


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(get_response(session, url).text, features)


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=({} if attrs is None else attrs))
    if searched_tag is None:
        raise ParserFindTagException(
            FIND_TAG_ERROR.format(tag=tag, attrs=attrs)
            )
    return searched_tag


def find_tags_by_selector(soup, selectors):
    tag = soup.select(selectors)
    if not tag:
        raise ParserFindTagException(
            FIND_TAGS_SELECTOR_ERROR.format(selectors=selectors)
            )
    return tag

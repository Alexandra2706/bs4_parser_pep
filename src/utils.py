import logging

from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(f'Возникла ошибка при загрузке страницы {url}',
                          stack_info=True)


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_list_status(soup):
    section_tag = find_tag(soup, 'section', {'id': 'pep-status-key'})
    em_tag = section_tag.find_all('em')
    status = [tag.text for tag in em_tag]
    return status


def get_pep_status(soup):
    section_tag = find_tag(soup, 'section', {'id': 'pep-content'})
    dl_tag = find_tag(section_tag, 'dl',
                      {'class': 'rfc2822 field-list simple'})
    dt_tags = dl_tag.find_all('dt')
    for dt_tag in dt_tags:
        if dt_tag.text == 'Status:':
            dd_tag = dt_tag.find_next_sibling()
            return dd_tag.text
    logging.info(f'Статус не найден {section_tag.h1.text}')

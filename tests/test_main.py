import pytest  
from unittest.mock import patch  
from main import main  
from utils import is_valid_url  


def test_main_success():  
    """Тестирует успешное выполнение функции main.  

    Проверяет, что функция main возвращает True, если:  
    - Функция get_sitemap_links успешно возвращает валидный URL.  
    - Функция check_link_status возвращает 200, указывая на то, что ссылка доступна.  
    - Функция fetch_page_content возвращает HTML, содержащий правильный canonical URL, который совпадает с запрашиваемым URL.  
    """  
    with patch('main.get_sitemap_links', return_value=['https://vikunja.io/docs/installing/']):  
        with patch('main.check_link_status', return_value=200):  
            with patch('main.fetch_page_content', return_value='<link rel="canonical" href="https://vikunja.io/docs/installing/"/>'):  
                result = main("https://vikunja.io/docs/installing/")  
                assert result is True  # Ожидается, что все проверки завершились успешно.  


def test_main_bad_links():  
    """Тестирует функцию main при наличии нерабочих ссылок.  

    Проверяет, что функция main возвращает False, если:  
    - Функция get_sitemap_links возвращает список ссылок.  
    - Функция check_link_status возвращает 404, указывая на то, что ссылка недоступна.  
    - Несмотря на наличие тега canonical в HTML-контенте, результат не должен быть успешным из-за статуса 404.  
    """  
    with patch('main.get_sitemap_links', return_value=['https://vikunja.io/docs/installing/']):  
        with patch('main.check_link_status', return_value=404):  
            with patch('main.fetch_page_content', return_value='<link rel="canonical" href="https://vikunja.io/docs/installing/"/>'):  
                result = main("https://vikunja.io/docs/installing/")  
                assert result is False  # Ожидается, что функция вернет False из-за недоступной ссылки.  


def test_main_canonical_errors():  
    """Тестирует функцию main на наличие ошибок в canonical URL.  

    Проверяет, что функция main возвращает False, если:  
    - Функция get_sitemap_links возвращает валидный URL.  
    - Функция check_link_status возвращает 200, указывая на то, что ссылка доступна.  
    - Однако тег canonical в HTML-контенте не совпадает с запрашиваемым URL, что свидетельствует о несоответствии.  
    """  
    with patch('main.get_sitemap_links', return_value=['https://vikunja.io/docs/installing/']):  
        with patch('main.check_link_status', return_value=200):  
            with patch('main.fetch_page_content', return_value='<link rel="canonical" href="https://vikunja.io/docs/"/>'):  # Ошибка в каноническом URL  
                result = main("https://vikunja.io/docs/installing/")  
                assert result is False  # Ожидается, что из-за ошибки canonical функция вернет False.  


def test_is_valid_url():  
    """Тестирует функцию валидации URL.  

    Проверяет, что функция is_valid_url возвращает:  
    - True для корректно сформированных URL, включая http и https.  
    - False для некорректных URL, такие как невалидные форматы и отсутствующие схемы.  
    """  
    assert is_valid_url("https://vikunja.io/docs/installing/") is True  # Валидный HTTPS URL  
    assert is_valid_url("http://vikunja.io/docs/installing/") is True  # Валидный HTTP URL  
    assert is_valid_url("ftp://vikunja.io/docs/installing/") is True  # Если FTP поддерживается  
    assert is_valid_url("invalid-url") is False  # Неверный URL без схемы  
    assert is_valid_url("http:/invalid-url.com") is False  # Неверный формат URL  
    assert is_valid_url("https://") is False  # Неполный URL  

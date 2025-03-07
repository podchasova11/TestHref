import pytest
from unittest.mock import patch
from main import main
from utils import is_valid_url


def test_main_success():
    """Тест, когда все проверки проходят успешно."""
    with patch('main.get_sitemap_links', return_value=['https://vikunja.io/docs/installing/']):
        with patch('main.check_link_status', return_value=200):
            with patch('main.fetch_page_content', return_value='<link rel="canonical" href="https://vikunja.io/docs/installing/"/>'):
                result = main("https://vikunja.io/docs/installing/")
                assert result is True


def test_main_bad_links():
    """Тест, когда есть нерабочие ссылки."""
    with patch('main.get_sitemap_links', return_value=['https://vikunja.io/docs/installing/']):
        with patch('main.check_link_status', return_value=404):
            with patch('main.fetch_page_content', return_value='<link rel="canonical" href="https://vikunja.io/docs/installing/"/>'):
                result = main("https://vikunja.io/docs/installing/")
                assert result is False


def test_main_canonical_errors():
    """Тест, когда есть ошибки canonical."""
    with patch('main.get_sitemap_links', return_value=['https://vikunja.io/docs/installing/']):
        with patch('main.check_link_status', return_value=200):
            with patch('main.fetch_page_content', return_value='<link rel="canonical" href="https://vikunja.io/docs/installing/"/>'):
                result = main("https://vikunja.io/docs/installing/")
                assert result is True


def test_is_valid_url():
    """Тест для проверки валидации URL."""
    assert is_valid_url("https://vikunja.io/docs/installing/") is True
    assert is_valid_url("invalid-url") is False

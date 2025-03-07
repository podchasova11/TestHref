import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def get_sitemap_links(url):
    """Получает все ссылки из sitemap.xml."""
    try:
        sitemap_url = urljoin(url, 'sitemap.xml')
        response = requests.get(sitemap_url)
        response.raise_for_status()  # Проверка на 200 OK
        soup = BeautifulSoup(response.content, 'xml')
        links = [loc.text for loc in soup.find_all('loc')]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении sitemap: {e}")
        return []


def get_all_links(url):
    """Получает все ссылки со страницы."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении ссылок со страницы: {e}")
        return []


def check_link_status(url):
    """Проверяет статус код ссылки."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException:
        return None


def check_canonical(url, page_content):
    """Проверяет rel="canonical" на странице."""
    soup = BeautifulSoup(page_content, 'html.parser')
    canonical_tag = soup.find('link', rel='canonical')
    if canonical_tag:
        return canonical_tag['href']
    return None


def fetch_page_content(url):
    """Получает контент страницы."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении контента страницы: {e}")
        return None


def is_valid_url(url):
    """Проверяет, является ли URL валидным."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

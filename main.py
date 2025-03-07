from urllib.parse import urlparse

from utils import get_sitemap_links, check_link_status, check_canonical, fetch_page_content, get_all_links, is_valid_url


def main(url):
    """Основная функция для проверки сайта."""
    sitemap_links = get_sitemap_links(url)
    all_links = []

    # Если sitemap недоступен, собираем все ссылки с главной страницы и следующих уровней
    if not sitemap_links:
        print("Sitemap не найден, собираем ссылки с сайта...")
        all_links.append(url)
        collected_links = set()
        for link in all_links:
            if link not in collected_links:
                collected_links.add(link)
                new_links = get_all_links(link)
                for new_link in new_links:
                    if is_valid_url(new_link) and urlparse(new_link).netloc == urlparse(url).netloc:  # Проверяем, что ссылка ведет на тот же домен
                        all_links.append(new_link)
        sitemap_links = list(collected_links)  # Используем собранные ссылки как sitemap_links

    bad_links = []
    canonical_errors = []

    with open("bad_links.txt", "w") as bad_links_file, open("canonical_errors.txt", "w") as canonical_errors_file:
        for link in sitemap_links:
            status_code = check_link_status(link)
            if status_code != 200:
                bad_links.append(f"{link} - {status_code}")
                bad_links_file.write(f"{link} - {status_code}\n")

            page_content = fetch_page_content(link)
            if page_content:
                canonical_url = check_canonical(link, page_content)
                if canonical_url and canonical_url != link:
                    canonical_errors.append(f"{link} - {canonical_url}")
                    canonical_errors_file.write(f"{link} - {canonical_url}\n")

    if bad_links:
        print("Обнаружены нерабочие ссылки:")
        for error in bad_links:
            print(error)
    else:
        print("Все ссылки в порядке (200 OK).")

    if canonical_errors:
        print("Обнаружены ошибки canonical:")
        for error in canonical_errors:
            print(error)
    else:
        print("Canonical URL в порядке.")

    return not (bad_links or canonical_errors)  # Возвращает True, если все проверки пройдены успешно


if __name__ == "__main__":
    target_url = "https://vikunja.io/docs/installing/"  # URL сайта
    result = main(target_url)
    if not result:
        exit(1)  # Выход с кодом ошибки, если есть несовпадения

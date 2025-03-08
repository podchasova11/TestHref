# TestHref
**1. Общая структура проекта:**

```
project_root/
├── main.py         # Основной скрипт, запускающий проверки
├── utils.py        # Вспомогательные функции (получение карты сайта, проверка ссылок, canonical)
├── tests/
│   ├── test_main.py  # Pytest тесты
├── requirements.txt # Зависимости
```

**2. Зависимости (requirements.txt):**

```
requests
beautifulsoup4
pytest
```

Установить их: `pip install -r requirements.txt`

 Я добавила обработку ситуации, когда `sitemap.xml` отсутствует. В этом случае скрипт будет пытаться собрать ссылки, начиная с главной страницы, и проверять их.
*   Добавлена функция `is_valid_url` для проверки валидности URL.

**Как использовать:**

1.  URL своего сайта в `main.py`.
2.  Запустить `main.py`.
3.  Проверь файлы `bad_links.txt` и `canonical_errors.txt` на наличие ошибок.
4.  Запустить тесты с помощью `pytest`.



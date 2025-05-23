# Поисковый микросервис на Flask

Простой, но функциональный бэкенд для имитации поискового сервиса, который генерирует "результаты" в виде ссылок с UUID.

## Структура проекта

```
project/
├── app.py                # Основное Flask-приложение
├── search_engine.py      # Логика поискового движка
├── response_collector.py # Скрипт для тестирования API
└── README.md             # Этот файл
```

## Зависимости

- Python 3.8+
- Установите зависимости:  
  ```bash
  pip install -r requirements.txt
  ```

## Как запустить

1. **Запустите сервер** (из корня проекта):
   ```bash
   python app.py
   ```
   Сервер будет доступен по адресу: `http://127.0.0.1:5005`

2. **Протестируйте API** (в другом терминале):
   ```bash
   python response_collector.py
   ```
   Скрипт отправит тестовые запросы и сохранит результаты в `result.json`.

## API Endpoints

### Поиск (`GET /api/search`)

**Параметры:**
- `query` (обязательный) — строка поискового запроса.

**Пример запроса:**
```bash
curl "http://127.0.0.1:5005/api/search?query=сигма"
```

**Пример ответа:**
```json
[
  "https://s3.ritm.media/hackaton-itmo/сигма/dee7518b-5f0c-4de7-a702-cb721e978661",
  "https://s3.ritm.media/hackaton-itmo/сигма/7a3e8f1d-2b4c-4e6f-9a1b-3c5d7e9f2a4b"
]
```

## Как это работает

### `app.py`
- Создает Flask-приложение.
- Регистрирует endpoint `/api/search`, который:
  - Принимает параметр `query`.
  - Передает запрос в `SearchEngine`.
  - Возвращает результаты в JSON.

### `search_engine.py`
- Имитирует поисковый движок:
  - Генерирует 10 случайных UUID для каждого запроса.
  - Формирует ссылки вида: `https://s3.ritm.media/hackaton-itmo/{uuid}`.

### `response_collector.py`
- Тестовый скрипт, который:
  - Отправляет запросы для слов из списка `query_list`.
  - Сохраняет все результаты в файл `result.json` (с кириллицей и форматированием).

## Пример результата (`result.json`)

После запуска `response_collector.py`:
```json
{
    "сигма": [
        "https://s3.ritm.media/hackaton-itmo/dee7518b-5f0c-4de7-a702-cb721e978661",
        "https://s3.ritm.media/hackaton-itmo/7a3e8f1d-2b4c-4e6f-9a1b-3c5d7e9f2a4b"
    ],
    "альтушка": [
        "https://s3.ritm.media/hackaton-itmo/3c8e1f9a-5b2d-4f6e-8a1c-6d3e9f2b5a4c"
    ]
}
```

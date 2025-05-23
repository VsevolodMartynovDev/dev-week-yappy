﻿# DewWeek2025

### 1. Клонируйте репозиторий

git clone https://github.com/Calcifer-02/DewWeek2025.git
cd DewWeek2025

##

### 2. Запустите бэкенд

pip install flask flask-cors
cd itmoexamplebackend
python app.py

### 3. Запустите фронтенд

Откройте index.html в браузере
Или используйте Live Server в VS Code

### 4. Проверьте поиск

Введите запрос в поле поиска
Бэкенд вернет 10 случайных ссылок

### Техническая информация

Фронтенд
Страницы:

/index.html - Главная

/search.html - Поиск

/upload.html - Загрузка видео

Стили: styles.css

Бэкенд
API: GET /api/search?query=...

Порт: 5005

Файлы:

app.py - Основной сервер

search_engine.py - Логика поиска

### Проблемы и решения

CORS-ошибки:

Убедитесь, что бэкенд запущен

Проверьте URL в браузере: http://localhost:5005/api/search?query=тест

Фронтенд не обновляется:

Очистите кэш браузера (Ctrl+F5)

Бэкенд не запускается:

Проверьте версию Python: python --version

Установите зависимости: pip install -r requirements.txt

# "YouGile" - Учебный репозиторий с UI и API тестами части основной 
# функциональности российской системы управления проектами YouGile
# ссылка - https://ru.yougile.com

## Шаблон для автоматизации тестирования на python

### Стек:
- pytest
- selenium
- requests
- allure
- config

### Структура:
- ./test - тесты
- ./pages - описание страниц

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore] (https://www.toptal.com/developers/gitignore)
### Шаги
1. Открыть терминал в доступном IDE
2. Перейти в папку в которой желаете разместить локальный репозиторий 
3. Склонировать проект командой 'git clone https://github.com/sdvoretskov-gif/
4. Установить зависимости
5. Запустить тесты 'pytest', 'pytest -m "ui"', 'pytest -m "api"'
6. Сгенерировать отчет 'allure generate allure-files -o allure-report'
7. Открыть отчет 'allure open allure-report'

### Библиотеки (!)
- pip install pytest
- pip install selenium
- pip install webdriver-manager
- pip install allure-pytest
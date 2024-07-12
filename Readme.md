# Тестовое задание от Фаблайт Электроникс
## Описание задания:
Разработать простое серверное приложение на выбранном вами языке программирования (Python или JavaScript).
Реализовать базу данных (можно использовать PostgreSQL или любую другую удобную вам систему).
Реализовать функции регистрации и аутентификации пользователей.
Реализовать обработку следующих типов запросов:
Получение списка пользователей.
Добавление нового пользователя.
Обновление информации о пользователе.
Удаление пользователя.
Обеспечить минимальную защиту приложения (например, защита от SQL-инъекций).

Критерии оценки тестового задания:
- Чистота и качество кода.
- Правильность и логичность реализации функционала.
- Способность обеспечить базовую защиту данных.
- Документация кода и комментарии.

## Реализация тестового задания
### Общий принцип работы приложения:
Приложение позволяет производить регистрацию, авторизацию
пользователей. Пользователи разделены на администраторов и
обычных пользователей. Для добавления первого администратора,
необходимо вручную изменить в бд таблицы поле is_admin на 1 (True).
Все пользователи изначально регистрируются без прав администратора.
Для выхода (разлогинивания) из системы необходимо нажать на
имя пользователя справа вверху. 
Обычным пользователям недоступны никакие права.
Под администратором можно добавлять новых пользователей, 
изменять имя и почту пользователей в системе, удалять пользователей,
а также назначать пользователей администраторами.
Администраторы видят список всех пользователей в системе.

### Запуск приложения
Для запуска приложения необходимо в terminal установить необходимые зависимости
командой __pip install -r requirements.txt__. После установки библиотек,
запустить файл __main.py__

### Структура приложения
Приложение состоит из следующих компонентов:
- Директория Data - содержит ORM модель таблицы пользователей (users.py) и файл
подключения к базе данных (db_session.py)
- Директория db - содержит файл базы данных sqlite. Базу данных 
можно отрыть с помощью приложения sqliteStudio (https://sqlitestudio.pl/).
Это обязательно необходимо сделать, так как первому созданному пользователю необходимо будет
назначить права администратора
- Директория forms содержит классы пользовательских форм, наследованных от
FlaskForm, это формы регистрации, авторизации и смены данных пользователя
- Директория templates содержит основные шаблоны - html документы, которые
рендерятся на эндпоинтах. __base.html__ - базовый шаблон, который расширяется
другими html-документа. В осномном, это header приложения.
__index.html__ - стартовая страница приложения. __login.html__ - страница авторизации.
__register.html__  - страница регистрации пользователя. __users.html__ - страница редактирования пользователя.
- файл .env - переменные окружения, такие как секретный ключ и длительность сессии.
- файл main.py - точка входа в приложение. Содержит базовые настройки flask-приложения,
 а также ключевые эндпоинты приложения.


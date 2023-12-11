# Django-project Mailing

Добро пожаловать!
Данный Django-проект представляет собой веб-приложение интернет-рассылок.

## Введение

Веб-приложение предназначено для работы с интернет-рассылками.


## Структура проекта

В файле README.md представлена общая информация о каждом файле и его 
назначении.

- manage.py - точка входа веб-приложения.
- requirements.txt - список зависимостей для проекта.
- .gitignore - для Python, MacOS

/config/
- 'settings.py' - настройки приложения.
- 'urls.py' - точка входа со стороны пользователя, маршрутизация.

/mailing/
- 'admin.py' - настройка административной панели.
- 'apps.py' - конфигурационный файл приложения.
- 'models.py' - модели приложения mailing.
- 'urls.py' - маршрутизация приложения.
- 'views.py' - контроллеры.

/mailing/migrations/
- миграции для приложения mailing.

Директории с шаблонами для приложения mailing. 
- /mailing/templates/mailing 
- /mailing/templates/mailing/includes

/mailing/templatetags/ - кастомные фильтры и теги.

/mailing/static/ - статические файлы.

## Установка

1. Клонируйте данный репозиторий на свой локальный компьютер.
2. Установите Python если он еще не установлен.
3. Установите и активируйте виртуальное окружение.
4. Перейдите в корневую папку проекта и установите все зависимости из файла requirements.txt
5. Создайте файл .env по шаблону .env.sample
6. Установите миграции: python3 manage.py migrate
7. Запустите кастомную команду чтобы создать супер пользователя: python3 manage.py csu
8. Запустите команду чтобы создать группу менеджеров: python3 manage.py create_manager
9. Запустите команду чтобы создать группу контент-менеджеров: python3 manage.py create_contentmanager
10. Запустите веб-приложение:
- либо через конфигурационные настройки PyCharm.
- либо через команду в терминале: python3 manage.py runserver

## Пример веб-приложения


![Снимок экрана 2023-12-11 в 16.21.40.png](..%2F..%2F..%2F..%2F%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202023-12-11%20%D0%B2%2016.21.40.png)



![Снимок экрана 2023-12-11 в 16.21.54.png](..%2F..%2F..%2F..%2F%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202023-12-11%20%D0%B2%2016.21.54.png)



## Ошибки и улучшения

Если вы обнаружили ошибки, у вас есть предложения по улучшению данного проекта
или у вас есть вопросы по использованию веб-приложения, пожалуйста, присылайте pull request.

# BigSurvey
Сервис проведения опросов и тестов, написанный на Python.
<p align="center">
<img src="https://img.shields.io/badge/made%20by-merlyan0-blue.svg" >
<img src="https://img.shields.io/github/last-commit/Merlyan0/BigSurvey" >
<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" >
</p>

## Описание
Проект предоставляет возможность пользователям проводить опросы и тесты. Написан на Python, использованы библиотеки Flask, Werkzeug, SQLAlchemy, WTForms.

## Запуск
### Запуск локально с целью тестирования/доработки
1. Скачайте весь проект целиком
2. Настройте виртуальное окружение. **Рекомендуется использовать Python версии 3.8 и выше.**
3. Установите необходимые библиотеки, используя requirements.txt
4. Запустите главный файл проекта - *app.py* <br>
<em>Готово! Проект запущен в вашей локальной сети и, вероятно, доступен по адресу: http://127.0.0.1:5000/.</em>
### Использование сайта
1. Перейдите по ссылке, указанной в информации о репозитории (http://bigsurvey.recipeguide.ru.xsph.ru/) <br>
<em>Готово! Вы можете полноценно тестировать и использовать сайт :)</em>


## Инструкция по использованию
### Навигация по главному меню
На любой странице сайта в самом верху есть главное меню.
Оно состоит из трёх кнопок: Главная, Создать опрос, Каталог опросов. Названия кнопок отражают их функцию.
### Создание опроса
1. Нажмите "Создать опрос" в главном меню
2. Откроется соответствующая форма, которую необходимо заполнить, согласно наименованиям полей
3. Нажмите "Сохранить"
4. Вас перенаправит на страницу редактирования опроса. Введите тот же пароль, что вы вводили в форме на 2-ом шаге <br>
<em>Готово! Опрос создан. Переходите к его настройке.</em>
### Настройка опроса, добавление/просмотр/удаление вопросов, просмотр результатов
1. После выполнения всех инструкций по созданию опроса вы оказались на странице редактирования. Она содержит 4 вкладки, на каждой из которых находится соответственно:
* Настройка приватности опроса
* Добавление новых вопросов
* Удаление и просмотр вопросов
* Просмотр результатов опроса <br>

Меню является интуитивно понятным, поэтому разобраться в нём не представляет сложности.
### Как поделиться опросом, чтобы его мог пройти другой пользователь
1. Зайдите в настройки опроса
2. Во вкладке "Общее" будет опубликована ссылка на ваш опрос. Её необходимо скопировать и отправить куда-либо. С ёё помощью любой пользователь сможет пройти опрос.

## Структура проекта
* *data* - модуль Python, отвечающий за работу с базой данных, а также все использующиеся модели
* *static* - папка со всеми статическими файлами: css, js, images и пр.
* *templates* - папка со всеми html-шаблонами
* *add_form.py* - форма создания нового опроса
* **app.py** - главный файл, содержащий весь основной код приложения Flask

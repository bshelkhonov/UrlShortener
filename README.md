# Сокращатель ссылок _ИзиСсылка_
Запуск:

``
pip install -r requirements.txt
``

``
python manager.py runserver
``

Запуск unit-тестов:

``
python testing.py
``

# Описание

_ИзиСсылка_ -- веб-сервис для сокращения ссылок. 

![](https://sun1-47.userapi.com/eUjXC4TuBhV79oSvU5gcb66u6YhhL-cbZcSXkA/wjE4aUd_JCs.jpg)

![](https://sun1-99.userapi.com/eQT-FXDys5ZFNKXSS8DXX9iD7n0PdSXuHa_W5A/5KTH99YiYog.jpg)

### Как генерируется ссылка: 

Выбирается случайное число от _0_ до _62^5 - 1_ и переводится в 62-ричную СС. 
Ссылки хранятся в базе данных SQLite. Также для зарегистрированных пользователей 
имеется возможность посмотреть свою историю и количество переходов по ссылкам.


### Использованные технологии:

- Flask -- бэкенд
- База данных SQLite -- хранение информации о ссылках и пользователях
- HTML, CSS и JS -- фронтэнд

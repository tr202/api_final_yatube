# api_final
api final для приложения yatube
### Технологии
Python 3.9
Django 3.2.16
DRF 3.12.4
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команды:
```
python3 manage.py migrate
python3 manage.py runserver
```
- Протестируйте одним из следующих запросов
```
http://127.0.0.1:8000/api/v1/posts/
http://127.0.0.1:8000/api/v1/groups/
http://127.0.0.1:8000/api/v1/follow/
```
- Автор Kostya
- tr202@ya.ru

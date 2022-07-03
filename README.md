### Цель проекта:

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий может быть расширен администратором.

### Как запустить проект:

```
git clone https://github.com/Hastred45/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 .\api_yamdb\manage.py  migrate
```

Запустить проект:

```
python3 .\api_yamdb\manage.py runserver
```

### Примеры работы API:

После запуска проекта откройте в браузере http://127.0.0.1:8000/redoc/

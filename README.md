# Yatube
## Описание проекта:
### Это социальная сеть где можноЖ
### создавать посты;
### подписываться/отписываться на авторов;
### оставлять к постам комментарии.

### Что бы апустить проект у себя на компьютере:
### Клонируйте репозиторий:
```sh
git clone https://github.com/nu-shtosh/hw05_final.git
```
### Создайте и активируйте виртуальное окружение:
```sh
python -m venv venv
source venv/Scripts/activate
```
### Установите зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```
### Выполните миграции и соберите статику проекта:
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```
### Запустите сервер:
```sh
python manage.py runserver
```

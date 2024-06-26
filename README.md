# Проект "QRKot"
Проект "QRKot" - спасите бедных котят.

### Автор:
- [Alibek Ubaidullayev] (https://github.com/alibekubaidullayev)

### Технологии:
- Python
- FastAPI
- SQLAlchemy

### Как клонировать репозиторий:

Перейдите в любуй папку куда вы хотели бы клонировать репозиторий и наберите следующую комманду:

```
git clone git@github.com:alibekubaidullayev/yamdb_final.git
```



### Что внутри .env:

.env файл содержит важную информацию, которую нельзя показывать публично
В нём содержаться следующие поля:
```
APP_TITLE=Сервис бронирования переговорных комнат
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret (любое секретное слово на выбор)
```


### Как запустить проект локально с помощью докера:

После того как вы клонировали репозиторий (см. выше) выполните слеующие комманды:

Перейти в директорию проекта:

```
cd cat_charity_fund
```


Создайте виртуальное окружение

```
python3 -m venv venv
```

Установите завимости
```
pip install -r requirements.txt
```

Запустите проект
```
uvicorn app.main:app
```

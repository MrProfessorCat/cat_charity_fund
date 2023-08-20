# Сервис CAT CHARITY FUND

**Source Code**: <a href="https://github.com/MrProfessorCat/cat_charity_fund" target="_blank">https://github.com/MrProfessorCat/cat_charity_fund</a>

---

Сервис представляет собой API для реализации фонда сбора пожертвований на различные целевые проекты


## Требования

Python 3.7+


## Установка


Склонируйте репозиторий и перейдите в него в командной строке:

```
git@github.com:MrProfessorCat/cat_charity_fund.git
```

Cоздайте и активируйте виртуальное окружение:

```
python3 -m venv venv
```
* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас Windows

    ```
    .\venv\Scripts\activate.bat
    ```


Обновите pip и установите зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустите приложение:

```
uvicorn app.main:app
```


```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>О команде <code>uvicorn main:app --reload</code>...</summary>

Команда `uvicorn main:app` означает следующее:

* `main`: файл `main.py`.
* `app`: объект, созданный внутри файла `main.py` в строчке `app = FastAPI()`.
* `--reload`: заставляет сервер перезапускаться при каждом изменении кода в проекте. Необходим на этапе разработки.

</details>

### Документация API

Откройте браузер <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Вы окажетесь на странице Swagger - инструмента для документирования и тестирования API.


### Альтернативная документация API

Перейдите на <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Вы увидите еще одну автоматически сгенерированную документацию (доступную через <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

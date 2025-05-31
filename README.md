# Spelling Bee

Игра на русском языке, где игроки составляют слова из предложенных букв с обязательным использованием центральной буквы.  
Цель — найти как можно больше слов и заработать очки по правилам.

---

## О проекте

- Проверка слов по русскому словарю.
- Поддержка истории найденных слов.
- Правила и счёт очков, аналогичные классической игре Spelling Bee.

---

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/yourusername/spelling-bee.git
    cd spelling-bee
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # Linux/macOS
    source venv/bin/activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

---

## Запуск приложения

```bash
flask run
```

По умолчанию приложение доступно по адресу:
http://127.0.0.1:5000/

## Структура проекта

spelling-bee/
├── app.py
├── main.py
├── requirements.txt
├── templates/
│ ├── end_game.html
│ ├── game.html
│ └── index.html
├── static/
│ └── style.css
└── zalizniak_lemmas_cleaned.pkl


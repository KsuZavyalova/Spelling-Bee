from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from main import SpellingBeeGame
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

RUSSIAN_LETTERS = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")


def generate_letters():
    for _ in range(100):
        center = random.choice(RUSSIAN_LETTERS)
        rest = list(set(RUSSIAN_LETTERS) - set(center))
        others = random.sample(rest, 6)
        game = SpellingBeeGame(center, others)
        session['total_possible'] = len(game.valid_words)
        if len(game.valid_words) >= 5:
            print(f"DEBUG: Буквы: {center} + {others}")
            print(f"DEBUG: Слова, подходящие к этим буквам ({len(game.valid_words)}):")
            print(", ".join(sorted(game.valid_words)))
            return center, others
    raise Exception("Не удалось найти подходящие буквы")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('index.html', error="Пожалуйста, введите имя.", username='', center_letter=None,
                                   other_letters=[])
        center_letter, other_letters = generate_letters()
        game = SpellingBeeGame(center_letter, other_letters)
        session['game_data'] = {
            'center': center_letter,
            'others': other_letters
        }
        session['found_words'] = []
        session['username'] = username
        app.config['game'] = game
        return redirect(url_for('game'))
    return render_template('index.html', username='', center_letter=None, other_letters=[], error=None)


@app.route('/game')
def game():
    username = session.get('username', 'Игрок')
    game_data = session.get('game_data')
    if not game_data:
        return redirect(url_for('index'))
    return render_template('game.html',
                           center_letter=game_data['center'],
                           other_letters=game_data['others'],
                           username=username,
                           total_possible=session.get('total_possible', 0),
                           found_words=session.get('found_words', []))


@app.route('/submit_word', methods=['POST'])
def submit_word():
    data = request.get_json()
    word = data.get("word", "").lower()
    game = app.config.get('game')
    if not game:
        return jsonify({"valid": False, "error": "Игра не инициализирована."})
    valid, message = game.submit_word(word)
    if valid:
        # обновляем найденные слова в сессии
        found_words = session.get('found_words', [])
        found_words.append(word)
        session['found_words'] = found_words
        return jsonify({
            "valid": True,
            "score": game.get_score(),
            "found_words": list(game.get_found_words()),
            "remaining": game.get_remaining(),
        })
    else:
        return jsonify({"valid": False, "error": message})


@app.route('/end_game')
def end_game():
    username = session.get('username', 'Игрок')
    game = app.config.get('game')
    score = game.get_score() if game else 0
    found_words = session.get('found_words', [])
    session.clear()
    app.config['game'] = None
    return render_template('end_game.html', username=username, score=score, found_words=found_words)


if __name__ == '__main__':
    app.run(debug=True)

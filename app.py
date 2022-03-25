from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    json = {"gameId": game_id, "board": game.board}
    return jsonify(json)

@app.post("/api/score-word")
def score_word():
    """ Checks word on board and return JSON {result: ok/not-word/not-on-board} """
    response = request.json
    game_id = response["gameId"]
    word = response["word"]
    # breakpoint()
    game = games[game_id]

    if not game.is_word_in_word_list(word):
        result = "not-word"
    elif not game.check_word_on_board(word):
        result = "not-on-board"
    else:
        result = "ok"
    json = {"result": result}

    print(json)

    return jsonify(json)


#       def is_word_in_word_list(self, word)
#     def check_word_on_board(self, word)

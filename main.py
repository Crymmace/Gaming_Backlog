import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/game_backlog"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String)
    genre = db.Column(db.String)

    def __init__(self, game, genre):
        self.game = game
        self.genre = genre


class Game:
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre

    def __repr__(self):
        return "{}, {}".format(self.name, self.genre)


def get_games():
    with app.app_context():
        all_games = []
        data = db.session.query(Data).filter().all()
        for row in data:
            temp_game = Game(row.game, row.genre)
            all_games.append(temp_game)
        return all_games


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    return flask.render_template("index.html")


@app.route("/view", methods=["GET", "POST"])
def view():
    all_games = get_games()
    if flask.request.method == "GET":
        return flask.render_template("view.html", all_games=all_games)


@app.route("/create", methods=["GET", "POST"])
def create():
    if flask.request.method == "GET":
        return flask.render_template("create.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    game = flask.request.form.get("g_name").title()
    genre = flask.request.form.get("genre").title()
    if flask.request.method == "POST":
        data = Data(game, genre)
        db.session.add(data)
        db.session.commit()
        return flask.render_template("submit.html")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if flask.request.method == "GET":
        return flask.render_template("delete.html")


@app.route("/remove", methods=["GET", "POST"])
def remove():
    game = flask.request.form.get("g_name").title()
    if flask.request.method == "POST":
        if db.session.query(Data).filter(Data.game == game).count() > 0:
            data = db.session.query(Data).filter(Data.game == game).first()
            db.session.delete(data)
            db.session.commit()
        return flask.render_template("remove.html")


if __name__ == "__main__":
    app.debug = True
    app.run()

#TODO: Implement API, make pretty, bug fixes, improve functionality, implement exporting

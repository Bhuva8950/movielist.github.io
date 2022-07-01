
from email.policy import default
from unicodedata import name
from flask import Flask, render_template, session, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Movies(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    time = db.Column(db.Integer, nullable=False, )
    location = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name}"


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/movies_list")
def movies_list():
    allmovie = Movies.query.all()
    if allmovie:
        return render_template("movieslist.html", allmovie=allmovie)
    else:
        msg = "No Movies in List pls add some movies"
        return render_template("movieslist.html", msg=msg)


@app.route("/add_movies", methods=["GET", "POST"])
def add_movies():
    if request.method == "POST":
        name = request.form["name"]
        time = request.form["time"]
        location = request.form["location"]

        movies = Movies(name=name, time=time, location=location)
        db.session.add(movies)
        db.session.commit()
        allmovie = Movies.query.all()

    return render_template("addmovies.html")


@app.route("/delete/<int:sno>")
def delete(sno):
    allmovie = Movies.query.filter_by(sno=sno).first()
    db.session.delete(allmovie)
    db.session.commit()
    return redirect("/movies_list")


@app.route("/edit/<int:sno>", methods=["GET", "POST"])
def edit(sno):
    if request.method=="POST":
        name = request.form["name"]
        time = request.form["time"]
        location = request.form["location"]
        movie = Movies.query.filter_by(sno=sno).first()
        movie.name=name
        movie.time=time
        movie.location=location
        db.session.add(movie)
        db.session.commit()
        return redirect ("/movies_list")

    movie = Movies.query.filter_by(sno=sno).first()
    return render_template("edit.html", movie=movie)


if __name__ == "__main__":
    app.run(debug=True)

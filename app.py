from flask import Flask, flash, redirect, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_db_connection():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row  # This enables name-based access to columns
    return conn

def initialize_db():
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
        CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()

initialize_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        score = request.form.get("score")

        if not name:
            flash("Name is required!")
            return redirect("/")
        if not score:
            flash("Score is required!")
            return redirect("/")

        try:
            score = int(score)
        except ValueError:
            flash("Score must be an integer!")
            return redirect("/")

        conn = get_db_connection()
        db = conn.cursor()
        db.execute(
            "INSERT INTO score (name, score) VALUES (?, ?)", (name, score)
        )
        conn.commit()
        conn.close()

        return redirect("/scores")
    else:
        return render_template("index.html")

@app.route("/scores")
def scores():
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("SELECT * FROM score")
    rows = db.fetchall()
    conn.close()
    return render_template("scores.html", scoreSheet=rows)

if __name__ == "__main__":
    app.run(debug=True)

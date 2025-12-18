from flask import (
    Flask, render_template, request,
    redirect, url_for, session, g, flash
)
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps

# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is not set")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
)

DATABASE = "namesprouts.db"

# =========================================================
# DATABASE HELPERS
# =========================================================

def get_db():
    if "_database" not in g:
        g._database = sqlite3.connect(DATABASE)
        g._database.row_factory = sqlite3.Row
        g._database.execute("PRAGMA foreign_keys = ON;")
    return g._database


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("_database", None)
    if db:
        db.close()


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name_text TEXT NOT NULL,
            month TEXT NOT NULL,
            flower_image TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    db.commit()

# =========================================================
# AUTH UTILITIES
# =========================================================

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def flower_image_path(month):
    path = f"flowers/{month}.png"
    full_path = os.path.join(app.static_folder, path)
    return f"static/{path}" if os.path.exists(full_path) else "static/flowers/default.png"

# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():
    return redirect(url_for("design")) if "user_id" in session else redirect(url_for("login"))

# ---------------- AUTH ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password")

        if not username or not email or not password:
            flash("All fields are required")
            return render_template("register.html")

        try:
            get_db().execute(
                "INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password))
            )
            get_db().commit()
        except sqlite3.IntegrityError:
            flash("Username or email already exists")
            return render_template("register.html")

        flash("Account created. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password")

        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if not user or not check_password_hash(user["hash"], password):
            flash("Invalid credentials")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session.permanent = True
        return redirect(url_for("design"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- DESIGN ---------------- #

@app.route("/design", methods=["GET", "POST"])
@login_required
def design():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        month = request.form.get("month")

        if not name or not month:
            flash("Name and month are required")
            return render_template("design.html")

        get_db().execute(
            """
            INSERT INTO projects (user_id, name_text, month, flower_image, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                name,
                month,
                flower_image_path(month),
                datetime.utcnow().isoformat()
            )
        )
        get_db().commit()
        return redirect(url_for("my_projects"))

    return render_template("design.html")

# ---------------- PROJECTS ---------------- #

@app.route("/my_projects")
@login_required
def my_projects():
    projects = get_db().execute(
        """
        SELECT *
        FROM projects
        WHERE user_id = ?
        ORDER BY creat



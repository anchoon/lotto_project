import sqlite3
import hashlib

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DB_FILE = "posts.db"

vegetables = [
    "토마토", "당근", "가지",
    "양파", "오이", "감자",
    "버섯", "배추", "브로콜리"
]

# =========================
# DB 초기화
# =========================

def init_db():

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nickname TEXT,

            content TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            views INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# 닉네임 생성
# =========================

def generate_nickname(ip):

    hash_value = int(
        hashlib.md5(ip.encode()).hexdigest(),
        16
    )

    veg = vegetables[
        hash_value % len(vegetables)
    ]

    number = hash_value % 100 + 1

    return f"{veg}{number}"

# =========================
# 글 저장
# =========================

def save_post(nickname, content):

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO posts
        (nickname, content)

        VALUES (?, ?)
        """,
        (nickname, content)
    )

    conn.commit()
    conn.close()

# =========================
# 글 불러오기
# =========================

def load_posts():

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            nickname,
            content,
            created_at,
            views

        FROM posts

        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return [

        {
            "id": r[0],
            "nickname": r[1],
            "text": r[2],
            "created_at": r[3],
            "views": r[4]
        }

        for r in rows
    ]

# =========================
# 메인
# =========================

@app.route("/")
def index():

    return render_template("index.html")

# =========================
# 게시판
# =========================

@app.route("/board", methods=["GET", "POST"])
def board():

    if request.method == "POST":

        content = request.form.get("content")

        if content and len(content) >= 10:

            ip = request.headers.get(
                "X-Forwarded-For",
                request.remote_addr
            )

            nickname = generate_nickname(ip)

            save_post(
                nickname,
                content
            )

        return redirect("/board")

    posts = load_posts()

    return render_template(
        "board.html",
        posts=posts
    )

# =========================
# 토토
# =========================

@app.route("/toto")
def toto():

    # 임시 데이터
    matches = [

        {
            "away": "KIA",
            "home": "롯데",
            "pitcher": "네일 vs 박세웅"
        },

        {
            "away": "LG",
            "home": "두산",
            "pitcher": "임찬규 vs 알칸타라"
        },

        {
            "away": "삼성",
            "home": "SSG",
            "pitcher": "원태인 vs 김광현"
        }

    ]

    return render_template(
        "toto.html",
        matches=matches
    )

# =========================

if __name__ == "__main__":

    app.run(debug=True)
import sqlite3
import hashlib
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB_FILE = "posts.db"

vegetables = ["토마토","당근","가지","양파","오이","감자","버섯","배추","브로콜리"]

# ---------------- DB ----------------
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

# ---------------- 닉네임 ----------------
def generate_nickname(ip):
    h = int(hashlib.md5(ip.encode()).hexdigest(), 16)
    return vegetables[h % len(vegetables)] + str(h % 100 + 1)

# ---------------- 게시글 저장 ----------------
def save_post(nickname, content):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO posts (nickname, content) VALUES (?, ?)",
        (nickname, content)
    )

    conn.commit()
    conn.close()

# ---------------- 게시글 조회 ----------------
def load_posts(page, per_page):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    offset = (page - 1) * per_page

    cur.execute("""
        SELECT id, nickname, content, created_at, views
        FROM posts
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset))

    rows = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM posts")
    total = cur.fetchone()[0]

    conn.close()

    posts = [
        {
            "id": r[0],
            "nickname": r[1],
            "text": r[2],
            "created_at": r[3],
            "views": r[4]
        }
        for r in rows
    ]

    return posts, total

# ---------------- BOARD ----------------
@app.route("/board", methods=["GET", "POST"])
def board():

    # 글 작성
    if request.method == "POST":
        content = request.form.get("content")

        if content and len(content) >= 10:
            ip = request.remote_addr
            nickname = generate_nickname(ip)

            save_post(nickname, content)

        return redirect("/board?success=1")

    # 페이지
    page = request.args.get("page", 1, type=int)
    per_page = 20

    posts, total = load_posts(page, per_page)

    has_next = page * per_page < total

    return render_template(
        "board.html",
        posts=posts,
        page=page,
        has_next=has_next,
        success=request.args.get("success")
    )

# ---------------- INDEX ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- TOTO ----------------
@app.route("/toto")
def toto():
    return render_template("toto.html")

if __name__ == "__main__":
    app.run(debug=True)
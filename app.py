from flask import Flask, render_template

app = Flask(__name__)

# 🎰 메인 로또
@app.route("/")
def index():
    return render_template("index.html")

# 📢 게시판
@app.route("/board")
def board():
    posts = []
    return render_template("board.html", posts=posts)

# ⚽ 스포츠토토
@app.route("/toto")
def toto():
    return render_template("toto.html")

if __name__ == "__main__":
    app.run(debug=True)
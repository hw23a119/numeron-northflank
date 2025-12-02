from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # ← 何でもいいので文字列を入れてください

# --- 答えを生成する関数 ---
def generate_answer():
    digits = list(range(10))
    random.shuffle(digits)
    return digits[:3]  # シャッフル後の先頭3つ（重複なし）

@app.route("/", methods=["GET", "POST"])
def index():
    # ユーザーごとの答えが無かったら生成
    if "answer" not in session:
        session["answer"] = generate_answer()
        session["history"] = []

    answer = session["answer"]
    history = session.get("history", [])
    result = ""
    
    if request.method == "POST":
        guess = request.form.get("guess", "")

        if len(guess) != 3 or not guess.isdigit():
            result = "⚠️ 3桁の数字を入力してください"
        else:
            guess_digits = [int(n) for n in guess]

            eat = sum(1 for i in range(3) if guess_digits[i] == answer[i])
            bite = sum(1 for n in guess_digits if n in answer) - eat

            if eat == 3:
                result = f"🎉 正解！ 答えは {''.join(map(str, answer))}"
            else:
                result = f"{eat} EAT, {bite} BITE"

            # 履歴更新
            history.insert(0, {"guess": guess, "eat": eat, "bite": bite})
            if len(history) > 5:
                history.pop()

            session["history"] = history

    return render_template("index.html", result=result, history=history)

@app.route("/hint")
def hint():
    if "answer" not in session:
        return redirect(url_for("index"))

    answer = session["answer"]

    # ランダムで1つヒントを出す
    idx = random.choice([0, 1, 2])
    hint_text = ["左の数字は ", "真ん中の数字は ", "右の数字は "][idx] + str(answer[idx])

    return redirect(url_for("index", hint=hint_text))

@app.route("/reset")
def reset():
    last_answer = ''.join(map(str, session.get("answer", [])))
    session["last_answer"] = last_answer

    session["answer"] = generate_answer()
    session["history"] = []

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

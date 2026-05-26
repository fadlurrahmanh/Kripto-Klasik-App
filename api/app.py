from flask import Flask, render_template, request, jsonify
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

history = []


# =========================
# HALAMAN
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/caesar")
def caesar():
    return render_template("caesar.html")


@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")


@app.route("/affine")
def affine():
    return render_template("affine.html")


@app.route("/hill")
def hill():
    return render_template("hill.html")


@app.route("/playfair")
def playfair():
    return render_template("playfair.html")


# =========================
# HISTORY
# =========================

@app.route("/history")
def show_history():
    return jsonify(history)


# =========================
# CAESAR PROCESS
# =========================

@app.route("/caesar/process", methods=["POST"])
def process_caesar():

    data = request.get_json()

    text = data["text"]
    shift = int(data["shift"])
    mode = data["mode"]

    if mode == "decrypt":
        shift = -shift

    result = ""
    steps = []

    for char in text:

        if char.isalpha():

            start = ord('A') if char.isupper() else ord('a')

            old = ord(char) - start
            new = (old + shift) % 26

            encrypted = chr(new + start)

            result += encrypted

            steps.append(
                f"{char} → ({old} + {shift}) mod 26 = {new} → {encrypted}"
            )

        else:
            result += char

    history.append({
        "cipher": "Caesar",
        "text": text,
        "result": result
    })

    return jsonify({
        "result": result,
        "steps": steps,
        "formula": "E(x) = (x + k) mod 26"
    })


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run()
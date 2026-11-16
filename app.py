# pyrefly: ignore [missing-import]
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def startseite():
    return render_template(
    "index.html",
    untertitel="Meine erste Flask-Seite."
)

if __name__ == "__main__":
    app.run(debug=True)
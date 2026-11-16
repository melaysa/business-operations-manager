from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def startseite():
    return render_template(
    "index.html",
    untertitel="Meine erste Flask-Seite."
)

@app.route("/status")
def statusseite():
    return render_template(
    "status.html",
        untertitel="Die Anwendung läuft."
    )
    
if __name__ == "__main__":
    app.run(debug=True)
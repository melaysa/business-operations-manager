# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for
from database import (
    create_tables,
    get_customers,
    get_customer,
    add_customer,
    update_customer,
    delete_customer,
)

app = Flask(__name__)


@app.route("/")
def startseite():
    return render_template("index.html", untertitel="Meine erste Flask-Seite.")


@app.route("/status")
def statusseite():
    return render_template("status.html", untertitel="Die Anwendung läuft.")


@app.route("/kunden", methods=["GET", "POST"])
def kunden_uebersicht():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        ansprechperson = request.form.get("ansprechperson", "").strip()

        if name and ansprechperson:
            add_customer(name, ansprechperson)

        return redirect(url_for("kunden_uebersicht"))

    kunden_liste = get_customers()
    return render_template("kunden.html", kunden=kunden_liste)


@app.route("/kunden/<int:customer_id>/bearbeiten", methods=["GET", "POST"])
def kunden_bearbeiten(customer_id):
    kunde = get_customer(customer_id)

    if kunde is None:
        return "Kunde nicht gefunden", 404

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        ansprechperson = request.form.get("ansprechperson", "").strip()

        if name and ansprechperson:
            update_customer(customer_id, name, ansprechperson)
            return redirect(url_for("kunden_uebersicht"))

    return render_template("kunde_bearbeiten.html", kunde=kunde)


@app.route("/kunden/<int:customer_id>/loeschen", methods=["POST"])
def kunden_loeschen(customer_id):
    delete_customer(customer_id)
    return redirect(url_for("kunden_uebersicht"))


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)

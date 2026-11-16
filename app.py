# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for
from database import (
    create_tables,
    get_customers,
    get_customer,
    add_customer,
    update_customer,
    delete_customer,
    get_orders,
    add_order,
    update_order_status
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
    if not delete_customer(customer_id):
        return "Dieser Kunde hat noch Aufträge und kann nicht gelöscht werden.", 409

    return redirect(url_for("kunden_uebersicht"))

@app.route("/auftraege", methods=["GET", "POST"])
def auftrags_uebersicht():
    kunden_liste = get_customers()

    if request.method == "POST":
        bezeichnung = request.form.get("bezeichnung", "").strip()
        kunde_id = request.form.get("kunde_id", type=int)

        if bezeichnung and kunde_id is not None:
            add_order(kunde_id, bezeichnung)

        return redirect(url_for("auftrags_uebersicht"))

    auftrags_liste = get_orders()
    return render_template(
        "auftraege.html",
        auftraege=auftrags_liste,
        kunden=kunden_liste,
    )
    
@app.route("/auftraege/<int:order_id>/status", methods=["POST"])
def auftrag_status_aendern(order_id):
    status = request.form.get("status", "")
    erlaubte_status = ("Offen", "In Bearbeitung", "Abgeschlossen")

    if status in erlaubte_status:
        update_order_status(order_id, status)

    return redirect(url_for("auftrags_uebersicht"))
    
if __name__ == "__main__":
    create_tables()
    app.run(debug=True)

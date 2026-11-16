import sqlite3

DATABASE_NAME = "business_operations.db"


def create_tables():
    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS kunden (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ansprechperson TEXT NOT NULL
        )
        """
    )

    anzahl = connection.execute("SELECT COUNT(*) FROM kunden").fetchone()[0]
    if anzahl == 0:
        connection.executemany(
            """
            INSERT INTO kunden (name, ansprechperson)
            VALUES (?, ?)
            """,
            [
                ("Nordlicht Service", "Mara Beispiel"),
                ("Werkstatt Morgenrot", "Timo Muster"),
            ],
        )

    connection.commit()
    connection.close()

def get_customer(customer_id):
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    customer = connection.execute(
        """
        SELECT id, name, ansprechperson
        FROM kunden
        WHERE id = ?
        """,
        (customer_id,),
    ).fetchone()

    connection.close()
    return customer
    
def get_customers():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    customers = connection.execute(
        "SELECT id, name, ansprechperson FROM kunden ORDER BY name"
    ).fetchall()

    connection.close()
    return customers

def add_customer(name, ansprechperson):
    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        """
        INSERT INTO kunden (name, ansprechperson)
        VALUES (?, ?)
        """,
        (name, ansprechperson),
    )

    connection.commit()
    connection.close()
    
def update_customer(customer_id, name, ansprechperson):
    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        """
        UPDATE kunden
        SET name = ?, ansprechperson = ?
        WHERE id = ?
        """,
        (name, ansprechperson, customer_id),
    )

    connection.commit()
    connection.close()
    
def delete_customer(customer_id):
    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        "DELETE FROM kunden WHERE id = ?",
        (customer_id,),
    )

    connection.commit()
    connection.close()

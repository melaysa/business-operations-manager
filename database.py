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
    
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS auftraege (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL,
            bezeichnung TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Offen',
            FOREIGN KEY (kunde_id) REFERENCES kunden(id)
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

def get_orders():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    orders = connection.execute(
        """
        SELECT auftraege.id, auftraege.bezeichnung, auftraege.status,
               kunden.name AS kundenname
        FROM auftraege
        JOIN kunden ON auftraege.kunde_id = kunden.id
        ORDER BY auftraege.id DESC
        """
    ).fetchall()

    connection.close()
    return orders

def add_order(kunde_id, bezeichnung):
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")

    connection.execute(
        """
        INSERT INTO auftraege (kunde_id, bezeichnung)
        VALUES (?, ?)
        """,
        (kunde_id, bezeichnung),
    )

    connection.commit()
    connection.close()
    
def update_order_status(order_id, status):
    connection = sqlite3.connect(DATABASE_NAME)

    connection.execute(
        "UPDATE auftraege SET status = ? WHERE id = ?",
        (status, order_id),
    )

    connection.commit()
    connection.close()
    

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
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        connection.execute(
            "DELETE FROM kunden WHERE id = ?",
            (customer_id,),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        connection.rollback()
        return False
    finally:
        connection.close()

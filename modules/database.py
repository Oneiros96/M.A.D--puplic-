import sqlite3
def init_database(db):
    table_setup(db)
    tables_setup(db)
    default_offers(db)
   

def table_setup(db):
    """Checks if all table's in offer.db in it are existing
    and creates them if not"""
    db.execute(
        "CREATE TABLE IF NOT EXISTS offers \
            (offer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, table_id INTEGER, name TEXT DEFAULT '' , price_netto NUMERIC DEFAULT 0.00, vat_rate NUMERIC DEFAULT '7%', price_brutto NUMERIC DEFAULT 0.00, description TEXT DEFAULT '')"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS tables (table_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name Text NOT NULL)"
    )
    db.execute("CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, street TEXT, street_nr TEXT, postal_code INTEGER, city TEXT)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS simplex_quotations (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, data TEXT)"
        )
    db.execute(
        "CREATE TABLE IF NOT EXISTS fabelzier_quotations (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, data TEXT)"
        )
    db.execute(
        "CREATE TABLE IF NOT EXISTS geierlamm_quotations (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, data TEXT)"
        )
    
def tables_setup(db):
    tables = db.execute("Select * FROM tables")
    if not tables:
        db.execute("INSERT INTO tables (name) VALUES ('Fabelzier')")
        db.execute("INSERT INTO tables (name) VALUES ('Geierlamm')")
        db.execute("INSERT INTO tables (name) VALUES ('Sonstiges')")



def default_offers(db):
    """ Checks if all db entrys needed for quotation creation are existing """
    journey  = db.execute(
        "SELECT * FROM offers WHERE offer_id = 1"
    )
    if not journey:
        db.execute(
            "INSERT INTO offers (name, price_netto, price_brutto, vat_rate, table_id, description) VALUES ('Anfahrt', 0.42, 0.45, '7%', 3, 'je km')"
        )
    else:
        if not journey[0]["name"] == "Anfahrt":
            db.execute(
                "UPDATE offers SET name = 'Anfahrt' WHERE offer_id = 1"
            )
        if not journey[0]["table_id"] == 3:
            db.execute(
                "UPDATE offers SET table_id = '3' WHERE offer_id = 1"
            )
    
    entertainer  = db.execute(
        "SELECT * FROM offers WHERE offer_id = 2"
    )
    if not entertainer:
        db.execute(
            "INSERT INTO offers (name, price_netto, price_brutto, vat_rate, table_id, description) VALUES ('Animateur', 158.88, 170, '7%', 3, 'je Tag')"
        )
    else:
        if not entertainer[0]["name"] == "Animateur":
            db.execute(
                "UPDATE offers SET name = 'Animateur' WHERE offer_id = 2"
            )
        if not entertainer[0]["table_id"] == 3:
            db.execute(
                "UPDATE offers SET table_id = '3' WHERE offer_id = 2"
            )
    
    construction  = db.execute(
        "SELECT * FROM offers WHERE offer_id = 3"
    )
    if not construction:
        db.execute(
            "INSERT INTO offers (name, price_netto, price_brutto, vat_rate, table_id) VALUES ('Auf- und Abbau', 336.45, 360, '7%', 3)"
        )
    else:
        if not construction[0]["name"] == "Auf- und Abbau":
            db.execute(
                "UPDATE offers SET name = 'Auf- und Abbau' WHERE offer_id = 3"
            )
        if not construction[0]["table_id"] == 3:
            db.execute(
                "UPDATE offers SET table_id = '3' WHERE offer_id = 3"
            )

class SQLite:
    """ Setup connection to database when needed and close it after querry.
    Results of querry's are returned as a list of dictionary's."""
    #  Init and specify db-file
    def __init__(self, database_file):
        self.database_file = database_file
        self.connection = None


    def connect(self):
        connection = sqlite3.connect(self.database_file)
        # print executed query's to console
        connection.set_trace_callback(print)
        return connection
    



    def execute(self, query, params=None):
        # create connection and cursor
        connection = self.connect()
        cursor = connection.cursor()
        # To make the output a list of dict's, with the Column names as keys
        cursor.row_factory = sqlite3.Row
        # Check if querry is an prepared statement and execute
        if params:
            cursor.execute(query, params)
            
        else:
            cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        # commit and close
        connection.commit()
        connection.close()
        return results

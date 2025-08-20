# init_db.py
import sqlite3

DB_NAME = "inventory.db"

# ---------- INITIALIZATION ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parts (
            part_id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_name TEXT NOT NULL,
            part_model TEXT NOT NULL,
            part_size TEXT,
            buy_price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            total_cost REAL GENERATED ALWAYS AS (buy_price * quantity) STORED,
            selling_price REAL NOT NULL,
            add_date TEXT DEFAULT CURRENT_DATE,
            add_time TEXT DEFAULT CURRENT_TIME,
            update_date TEXT,
            update_time TEXT
        )
    """)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_history (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT NOT NULL,
           login_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_history (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_id INTEGER,                 -- ID of the part sold (can be NULL for custom items)
            part_name TEXT,                  -- Name of the part or custom item
            quantity INTEGER,                -- Quantity sold
            price REAL,                      -- Price per unit
            total REAL,                      -- Total price for this item (qty * price)
            sale_date TEXT DEFAULT CURRENT_DATE,  -- Sale date
            sale_time TEXT DEFAULT CURRENT_TIME,  -- Sale time
            sold_by TEXT NOT NULL             -- Username of the person who made the sale
        )
    """)
    

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")


# ---------- QUERY FUNCTIONS ----------
def get_all_parts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT part_id, part_name, part_model, selling_price FROM parts")
    data = cursor.fetchall()
    conn.close()
    return data


def get_part_by_id(part_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT part_name, part_model, selling_price FROM parts WHERE part_id=?", (part_id,))
    part = cursor.fetchone()
    conn.close()
    return part


def insert_sale(part_id, part_name, quantity, price, sold_by):
    """
    Insert a sale record into sales_history table.
    `total` is calculated automatically as quantity * price.
    `sale_date` and `sale_time` use default current date/time.
    """
    total = quantity * price
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sales_history (part_id, part_name, quantity, price, total, sold_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (part_id, part_name, quantity, price, total, sold_by))
    conn.commit()
    conn.close()
    
def get_last_logged_user():
    import sqlite3
    conn = sqlite3.connect(DB_NAME)  # update with your DB path
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username FROM login_history
        ORDER BY login_time DESC
        LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
    
def get_part_quantity(part_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM parts WHERE part_id=?", (part_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def update_part_quantity(part_id, new_qty):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE parts SET quantity=? WHERE part_id=?", (new_qty, part_id))
    conn.commit()
    conn.close()


# Run DB init when script is executed directly
if __name__ == "__main__":
    init_db()

# db_parts.py
import sqlite3

DB = "inventory.db"

def get_all_parts():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM parts")
        return cursor.fetchall()

def delete_part(part_id):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM parts WHERE part_id = ?", (part_id,))
        conn.commit()

def update_quantity(part_id, new_quantity):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        
        # Get current quantity
        cursor.execute("SELECT quantity FROM parts WHERE part_id = ?", (part_id,))
        result = cursor.fetchone()
        
        if result is None:
            print("Part not found.")
            return
        
        current_quantity = result[0]
        total_quantity = current_quantity + new_quantity

        # Update with new total quantity
        cursor.execute("""
            UPDATE parts SET 
                quantity = ?, 
                update_date = CURRENT_DATE, 
                update_time = CURRENT_TIME 
            WHERE part_id = ?
        """, (total_quantity, part_id))
        conn.commit()

def update_part(part_id, data):
  with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE parts SET 
                part_name = ?, 
                part_model = ?, 
                part_size = ?, 
                buy_price = ?, 
                selling_price = ?, 
                update_date = CURRENT_DATE, 
                update_time = TIME('now', 'localtime')
            WHERE part_id = ?
        """, (*data, part_id))
        conn.commit()

def insert_part(data):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO parts 
                (part_name, part_model, part_size, buy_price, quantity, selling_price, add_date, add_time)
            VALUES (?, ?, ?, ?, ?, ?, DATE('now'), TIME('now','localtime'))
        """, data)
        conn.commit()

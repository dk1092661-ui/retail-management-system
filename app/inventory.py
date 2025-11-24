# app/inventory.py

from app.database import get_connection

def add_product(name, category, price, stock):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        (name, category, price, stock)
    )
    conn.commit()
    conn.close()


def get_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price, stock FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_product(product_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def update_product_stock(product_id, new_stock):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE products SET stock = ? WHERE id = ?",
        (new_stock, product_id)
    )
    conn.commit()
    conn.close()

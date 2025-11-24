# app/sales.py
from app.database import get_connection

def record_sale(product_id, quantity, total_price, date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO sales (product_id, quantity, total_price, date) VALUES (?, ?, ?, ?)",
        (product_id, quantity, total_price, date)
    )

    conn.commit()
    conn.close()


def get_all_sales():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sales.id, products.name, sales.quantity, sales.total_price, sales.date
        FROM sales
        INNER JOIN products ON sales.product_id = products.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

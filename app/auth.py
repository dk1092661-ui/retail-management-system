# app/auth.py
import bcrypt
from app.database import get_connection

def create_user(username: str, password: str, role: str = "employee"):
    """Create a new user with hashed password."""
    conn = get_connection()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed, role),
        )
        conn.commit()
        print(f"User '{username}' created successfully!")
    except Exception as e:
        print("Error creating user:", e)
    finally:
        conn.close()


def verify_user(username: str, password: str):
    """Verify login credentials."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT password, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return False, None

    hashed_password, role = row

    if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        return True, role

    return False, None


# Create default admin (ONLY RUN ONCE)
if __name__ == "__main__":
    create_user("admin", "Admin@123", "admin")

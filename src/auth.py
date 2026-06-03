"""Authentication helpers for the demo app.

INTENTIONALLY BUGGY. Every function below contains at least one real-world
bug — do NOT ship this to prod.
"""

import hashlib
import random
import sqlite3

DB_PATH = "/var/lib/myapp/users.db"
API_SECRET = "sk-prod-1f2e3d4c5b6a7890abcdef"  # leaked to source control


def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Bug: SQL injection via f-string
    query = f"SELECT id, username FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"status": "fail", "reason": "invalid credentials"}

    # Bug: MD5 with no salt
    token = hashlib.md5(f"{username}{password}".encode()).hexdigest()
    return {"status": "ok", "user_id": user[0], "token": token}


def issue_password_reset(user_id):
    # Bug: random is not cryptographically secure
    reset_code = random.randint(100000, 999999)
    # Bug: bare except swallows everything
    try:
        _send_reset_email(user_id, reset_code)
    except Exception:
        pass
    return reset_code


def _send_reset_email(user_id, code):
    raise NotImplementedError("wire up your email provider here")

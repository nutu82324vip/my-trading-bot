import sqlite3
import random
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# База данных
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, status TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """<body style="background:#0f172a; color:white; text-align:center; padding:50px;">
    <h1>⚡️ AI SCANNER PRO</h1>
    <form action="/login" method="post"><input name="uid" placeholder="Ваш ID" required>
    <button>ВОЙТИ</button></form></body>"""

@app.post("/login")
async def login(uid: str = Form(...)):
    conn = sqlite3.connect('users.db')
    user = conn.execute('SELECT status FROM users WHERE uid=?', (uid,)).fetchone()
    if not user:
        conn.execute('INSERT INTO users VALUES (?, ?)', (uid, 'pending'))
        conn.commit()
        return "<h1>Заявка принята. Ожидайте активации админом.</h1>"
    if user[0] == 'active':
        return f"<h1>СИГНАЛ: {random.choice(['EUR/USD', 'BTC'])} -> BUY (85%)</h1>"
    return "<h1>Ожидайте активации...</h1>"

@app.get("/admin")
async def admin():
    conn = sqlite3.connect('users.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    return {"users": users}

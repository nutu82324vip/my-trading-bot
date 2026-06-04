from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <body style="background:#0a0a0c; color:#fff; font-family:sans-serif; text-align:center;">
            <h1>QUANTUM CORE v4.2</h1>
            <button onclick="alert('Сканер запущен!')" style="padding:20px; background:#00ffcc; border:none; border-radius:10px; font-weight:bold;">📷 ВКЛЮЧИТЬ AR-СКАНЕР</button>
        </body>
    </html>
    """

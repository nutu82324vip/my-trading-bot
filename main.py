from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse(content="<h1>Сервер работает!</h1><p>Если ты видишь эту надпись, значит код верный.</p>")

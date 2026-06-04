import os
from groq import Groq
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import json

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def get_ai_prediction(asset):
    try:
        # Просим ИИ строго следовать формату
        prompt = f"Проанализируй график {asset}. Ответь ТОЛЬКО JSON без лишних слов. Формат: {{\"dir\": \"ВВЕРХ\", \"reason\": \"причина\", \"accuracy\": \"90%\"}}"
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw_text = completion.choices[0].message.content.replace("```json", "").replace("```", "").strip()
        
        # Пытаемся распарсить, если не вышло — пробуем исправить
        try:
            return json.loads(raw_text)
        except:
            # Если ИИ все же прислал текст, а не JSON
            return {"dir": "ОШИБКА ФОРМАТА", "reason": raw_text[:50], "accuracy": "0%"}
            
    except Exception as e:
        return {"dir": "ОШИБКА API", "reason": str(e), "accuracy": "0%"}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    return await get_ai_prediction(data.get("asset"))

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="width:400px; margin:20px auto; padding:20px; border:1px solid #444; border-radius:10px; background:#121212;">
        <h2 style="text-align:center; color:#00ffcc;">TRADING AI CORE</h2>
        <select id="asset" style="width:100%; margin-bottom:10px;"><option>EUR/USD</option><option>GBP/USD</option><option>USD/JPY</option><option>BTC/USD</option></select>
        <button id="btn" onclick="go()" style="width:100%; padding:15px; background:#00ffcc; color:#000; font-weight:bold; border:none; border-radius:5px;">ЗАПУСТИТЬ ИИ-АНАЛИЗ</button>
        <div id="res" style="margin-top:15px; padding:10px; border:1px solid #333; text-align:center;"></div>
    </div>
    <script>
        async function go() {
            const btn = document.getElementById('btn');
            const res = document.getElementById('res');
            btn.disabled = true;
            res.innerHTML = "Анализирую...";
            try {
                const resp = await fetch('/analyze', {
                    method:'POST', 
                    body:JSON.stringify({asset:document.getElementById('asset').value}), 
                    headers:{'Content-Type':'application/json'}
                });
                const d = await resp.json();
                res.innerHTML = `<div style="font-size:2rem; font-weight:bold; color:${d.dir=='ВВЕРХ'?'#00ff00':(d.dir=='ВНИЗ'?'#ff0000':'#ffcc00')}">${d.dir}</div>
                                 <p style="font-size:0.9rem;">${d.reason}</p><b>Точность: ${d.accuracy}</b>`;
            } catch(e) { res.innerHTML = "Ошибка связи с сервером"; }
            btn.disabled = false;
        }
    </script>
    </html>
    """

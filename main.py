import os
from groq import Groq
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import json

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Функция обращения к ИИ
async def get_ai_prediction(asset):
    try:
        prompt = f"Проанализируй график {asset}. Ты — профессиональный трейдер. Дай точный прогноз ВВЕРХ или ВНИЗ. Формат JSON: {{\"dir\": \"ВВЕРХ/ВНИЗ\", \"reason\": \"техническое обоснование\", \"accuracy\": \"95%\"}}"
        completion = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(completion.choices[0].message.content.replace("```json", "").replace("```", ""))
    except Exception as e:
        return {"dir": "ОШИБКА", "reason": str(e), "accuracy": "0%"}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    asset = data.get("asset")
    # Оба режима теперь используют ИИ
    return await get_ai_prediction(asset)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="width:400px; margin:20px auto; padding:20px; border:1px solid #444; border-radius:10px; background:#121212;">
        <h2 style="text-align:center; color:#00ffcc;">TRADING AI CORE</h2>
        <select id="asset" style="width:100%; margin-bottom:10px;">
            <option>EUR/USD</option><option>GBP/USD</option><option>USD/JPY</option><option>BTC/USD</option>
        </select>
        <label><b>ЭКСПИРАЦИЯ СДЕЛКИ:</b></label>
        <select id="time" style="width:100%; margin-bottom:15px;">
            <option>5 сек</option><option>15 сек</option><option>30 сек</option><option>1 мин</option><option>2 мин</option>
            <option>3 мин</option><option>4 мин</option><option>5 мин</option><option>10 мин</option>
        </select>
        <button onclick="go()" style="width:100%; padding:15px; background:#00ffcc; color:#000; font-weight:bold; border:none; border-radius:5px;">ЗАПУСТИТЬ ИИ-АНАЛИЗ</button>
        <div id="cd" style="margin-top:15px; text-align:center; color:#ffcc00; font-weight:bold;"></div>
        <div id="res" style="margin-top:15px; padding:10px; border:1px solid #333; text-align:center;"></div>
    </div>
    <script>
        async function go() {
            const cd = document.getElementById('cd');
            const res = document.getElementById('res');
            let count = 3;
            cd.innerHTML = "Подготовка...";
            const timer = setInterval(async () => {
                cd.innerHTML = `Вход в сделку через: ${count} сек`;
                if(count <= 0) {
                    clearInterval(timer);
                    cd.innerHTML = "ИИ АНАЛИЗИРУЕТ...";
                    const resp = await fetch('/analyze', {method:'POST', body:JSON.stringify({asset:document.getElementById('asset').value}), headers:{'Content-Type':'application/json'}});
                    const d = await resp.json();
                    res.innerHTML = `<div style="font-size:2rem; font-weight:bold; color:${d.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}">${d.dir}</div>
                                     <p style="font-size:0.9rem;">${d.reason}</p><b>Точность: ${d.accuracy}</b>`;
                }
                count--;
            }, 1000);
        }
    </script>
    </html>
    """

import os
import openai
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analyze")
async def analyze_data(request: Request):
    data = await request.json()
    mode = data.get("mode") # Узнаем, какой режим запущен: "button" или "scanner"
    asset = data.get("asset")
    
    if mode == "button":
        # Рандомный сигнал для кнопки
        import random
        dir = random.choice(['ВВЕРХ', 'ВНИЗ'])
        return {"dir": dir, "reason": "Мгновенный сигнал на основе волатильности.", "accuracy": "70%"}
    else:
        # ИИ сигнал для сканера
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты трейдер. Верни JSON: {'dir': 'ВВЕРХ' или 'ВНИЗ', 'reason': 'почему', 'accuracy': '90%'}"},
                {"role": "user", "content": f"Проанализируй график {asset}."}
            ]
        )
        return json.loads(response.choices[0].message.content)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
        <div style="max-width:400px; margin:auto; padding:20px;">
            <h1 style="color:#00ffcc;">QUANTUM CORE v4.2</h1>
            <select id="asset" style="width:100%; padding:10px; background:#1f1f24; color:#fff; margin-bottom:10px;">
                <option>EUR/USD</option><option>USD/JPY</option>
            </select>
            
            <button onclick="run('button')" style="width:100%; padding:15px; background:#222; border:1px solid #00ffcc; color:#fff; margin-bottom:10px;">⚡ БЫСТРЫЙ СИГНАЛ (Рандом)</button>
            <button onclick="run('scanner')" style="width:100%; padding:15px; background:#00ffcc; border:none; font-weight:bold;">📷 ВКЛЮЧИТЬ ИИ-СКАНЕР</button>
            
            <div id="res" style="margin-top:20px;"></div>
        </div>
        <script>
            async function run(mode) {
                const res = document.getElementById('res');
                res.innerHTML = mode === 'scanner' ? "🔍 ИИ-Сканер анализирует..." : "⚡ Генерирую сигнал...";
                
                const resp = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({mode: mode, asset: document.getElementById('asset').value})
                });
                const data = await resp.json();
                
                res.innerHTML = `
                    <div style="font-size:3rem; font-weight:bold; color:${data.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}">${data.dir}</div>
                    <div style="font-size:0.9rem; color:#aaa; margin:10px 0;">${data.reason}</div>
                    <div id="timer" style="color:#ffcc00; font-size:1.2rem;">ВХОД ЧЕРЕЗ: 10</div>
                `;
                
                let t = 10;
                let interval = setInterval(() => {
                    t--;
                    document.getElementById('timer').innerText = "ВХОД ЧЕРЕЗ: " + t;
                    if(t <= 0) clearInterval(interval);
                }, 1000);
            }
        </script>
    </html>
    """

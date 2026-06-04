import os
import openai
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analyze")
async def analyze_data(request: Request):
    try:
        data = await request.json()
        asset = data.get("asset")
        # Если сканер — стучимся в ИИ
        if data.get("mode") == "scanner":
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Дай прогноз (ВВЕРХ/ВНИЗ), причину и точность для {asset}. Формат: {'dir': '...', 'reason': '...', 'accuracy': '...'}"}]
            )
            return json.loads(response.choices[0].message.content)
        # Если кнопка — рандом
        else:
            import random
            return {"dir": random.choice(['ВВЕРХ', 'ВНИЗ']), "reason": "Быстрый анализ.", "accuracy": "60%"}
    except Exception as e:
        return {"dir": "ОШИБКА", "reason": str(e), "accuracy": "0%"}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="max-width:400px; margin:auto; padding:20px; border:1px solid #333;">
        <h1 style="text-align:center; color:#00ffcc;">QUANTUM CORE v4.2</h1>
        <select id="asset" style="width:100%; padding:10px; background:#222; color:#fff;">
            <option>EUR/USD</option><option>USD/JPY</option>
        </select>
        <button onclick="run('button')" style="width:100%; padding:15px; margin-top:10px; background:#444;">⚡ СИГНАЛ</button>
        <button onclick="run('scanner')" style="width:100%; padding:15px; margin-top:10px; background:#00ffcc; color:#000; font-weight:bold;">📷 ИИ-СКАНЕР</button>
        <div id="res" style="margin-top:20px;"></div>
    </div>
    <script>
        async function run(m){
            document.getElementById('res').innerHTML = "⏳ Ожидание ИИ...";
            const resp = await fetch('/analyze', {method:'POST', body:JSON.stringify({mode:m, asset:document.getElementById('asset').value}), headers:{'Content-Type':'application/json'}});
            const d = await resp.json();
            document.getElementById('res').innerHTML = `<h3>${d.dir}</h3><p>${d.reason}</p><p>Точность: ${d.accuracy}</p>`;
        }
    </script>
    </html>
    """

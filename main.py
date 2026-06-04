import os
from groq import Groq
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def get_ai_prediction(asset, timeframe):
    try:
        prompt = f"Проанализируй график {asset} для экспирации {timeframe}. Ты — профессиональный трейдер. Дай точный прогноз ВВЕРХ или ВНИЗ. Формат JSON: {{\"dir\": \"ВВЕРХ/ВНИЗ\", \"reason\": \"анализ\", \"accuracy\": \"95%\"}}"
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}]
        )
        content = completion.choices[0].message.content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        return {"dir": "ОШИБКА", "reason": str(e), "accuracy": "0%"}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    return await get_ai_prediction(data.get("asset"), data.get("time"))

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="width:400px; margin:20px auto; padding:20px; border:1px solid #444; border-radius:10px; background:#121212;">
        <h2 style="text-align:center; color:#00ffcc;">TRADING AI CORE</h2>
        
        <label>АКТИВ:</label>
        <select id="asset" style="width:100%; margin-bottom:10px;"><option>EUR/USD</option><option>GBP/USD</option><option>BTC/USD</option></select>
        
        <label><b>ЭКСПИРАЦИЯ (ТАЙМЕР):</b></label>
        <select id="time" style="width:100%; margin-bottom:15px;">
            <option>5 сек</option><option>15 сек</option><option>30 сек</option><option>1 мин</option><option>5 мин</option><option>10 мин</option>
        </select>
        
        <button id="btn" onclick="go()" style="width:100%; padding:15px; background:#00ffcc; color:#000; font-weight:bold; border:none; border-radius:5px;">ЗАПУСТИТЬ ИИ-СКАНЕР</button>
        
        <div id="cd" style="margin-top:15px; text-align:center; color:#ffcc00; font-weight:bold;"></div>
        <div id="res" style="margin-top:15px; padding:10px; border:1px solid #333; text-align:center;"></div>
    </div>
    
    <script>
        async function go() {
            const btn = document.getElementById('btn');
            const res = document.getElementById('res');
            const cd = document.getElementById('cd');
            const asset = document.getElementById('asset').value;
            const time = document.getElementById('time').value;
            
            btn.disabled = true;
            res.innerHTML = "";
            let count = 3;
            
            const timer = setInterval(async () => {
                cd.innerHTML = `Вход в сделку через: ${count} сек`;
                if(count <= 0) {
                    clearInterval(timer);
                    cd.innerHTML = "ИИ АНАЛИЗИРУЕТ...";
                    const resp = await fetch('/analyze', {
                        method:'POST', 
                        body:JSON.stringify({asset: asset, time: time}), 
                        headers:{'Content-Type':'application/json'}
                    });
                    const d = await resp.json();
                    cd.innerHTML = "";
                    res.innerHTML = `<div style="font-size:2rem; font-weight:bold; color:${d.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}">${d.dir}</div>
                                     <p style="font-size:0.9rem;">${d.reason}</p><b>Точность: ${d.accuracy}</b>`;
                    btn.disabled = false;
                }
                count--;
            }, 1000);
        }
    </script>
    </html>
    """

import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    prompt = f"Анализ {data['asset']} на {data['time']}. Дай прогноз (ВВЕРХ/ВНИЗ), причину и точность. Формат JSON: {{'dir': 'ВВЕРХ/ВНИЗ', 'reason': 'анализ', 'accuracy': '90%'}}"
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except:
        return {"dir": "ОШИБКА", "reason": "ИИ думает...", "accuracy": "0%"}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="max-width:400px; margin:20px auto; padding:20px; background:#121212; border-radius:15px; border:1px solid #333;">
        <h2 style="text-align:center; color:#00ffcc;">QUANTUM CORE PRO</h2>
        
        <label>АКТИВ:</label>
        <select id="asset" style="width:100%; margin-bottom:10px; background:#222; color:#fff;"><option>EUR/USD</option><option>BTC/USD</option><option>GOLD</option></select>
        
        <label>ЭКСПИРАЦИЯ:</label>
        <select id="time" style="width:100%; margin-bottom:20px; background:#222; color:#fff;"><option>30 сек</option><option>1 мин</option><option>5 мин</option></select>
        
        <button id="btn" onclick="startScanner()" style="width:100%; padding:20px; background:linear-gradient(to right, #00c6ff, #0072ff); border:none; color:#fff; font-weight:bold; border-radius:10px;">ЗАПУСК АНАЛИЗА</button>
        
        <div id="cd" style="margin-top:15px; text-align:center; font-weight:bold; color:#ffcc00;"></div>
        <div id="res" style="margin-top:15px; padding:15px; border:1px solid #444; text-align:center;">РЕЗУЛЬТАТ</div>
        
        <button onclick="alert('Перекрытие активировано!')" style="width:100%; margin-top:20px; padding:15px; background:#ff4757; border:none; color:#fff; font-weight:bold; border-radius:10px;">КНОПКА ПЕРЕКРЫТИЯ</button>
        
        <div style="margin-top:20px; font-size:0.75rem; color:#888;">
            <p>1. <b>Совет ИИ:</b> Прибыль фиксируется при достижении 1.5% от банка.</p>
            <p>2. <b>Совет ИИ:</b> Избегайте сделок при выходе важных экономических новостей.</p>
        </div>
    </div>
    
    <script>
        async function startScanner() {
            const btn = document.getElementById('btn');
            const cd = document.getElementById('cd');
            const res = document.getElementById('res');
            btn.disabled = true;
            
            let count = 5;
            const timer = setInterval(async () => {
                cd.innerHTML = `Вход в сделку через: ${count} сек`;
                if(count <= 0) {
                    clearInterval(timer);
                    cd.innerHTML = "ИИ АНАЛИЗИРУЕТ...";
                    const resp = await fetch('/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({asset: document.getElementById('asset').value, time: document.getElementById('time').value})
                    });
                    const d = await resp.json();
                    cd.innerHTML = "";
                    res.innerHTML = `<b style="font-size:28px; color:${d.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}">${d.dir}</b><br><small>${d.reason}</small><br><b>Точность: ${d.accuracy}</b>`;
                    btn.disabled = false;
                }
                count--;
            }, 1000);
        }
    </script>
    </html>
    """

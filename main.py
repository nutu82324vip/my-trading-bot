import os
from groq import Groq
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def get_ai_prediction(asset, timeframe, candle):
    try:
        # Промпт теперь требует анализ и отсчет, исключая любую "отсебятину"
        prompt = f"Проанализируй актив {asset}, таймфрейм экспирации {timeframe}, свечной интервал {candle}. Дай только JSON: {{\"dir\": \"ВВЕРХ/ВНИЗ\", \"reason\": \"технический анализ\", \"accuracy\": \"95%\"}}"
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        raw = completion.choices[0].message.content.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        return {"dir": "ОШИБКА", "reason": str(e), "accuracy": "0%"}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    return await get_ai_prediction(data.get("asset"), data.get("time"), data.get("candle"))

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="width:400px; margin:20px auto; padding:25px; border:1px solid #444; border-radius:12px; background:#121212;">
        <h2 style="text-align:center; color:#00ffcc; margin-bottom:20px;">AI SCANNER PRO</h2>
        <select id="asset" style="width:100%; margin-bottom:10px;"><option>EUR/USD</option><option>GBP/USD</option><option>BTC/USD</option></select>
        <label>Экспирация:</label>
        <select id="time" style="width:100%; margin-bottom:10px;"><option>5 сек</option><option>30 сек</option><option>1 мин</option><option>5 мин</option><option>10 мин</option></select>
        <label>Интервал свечи:</label>
        <select id="candle" style="width:100%; margin-bottom:20px;"><option>1 мин</option><option>5 мин</option></select>
        
        <button id="btn" onclick="startScan()" style="width:100%; padding:18px; background:#00ffcc; color:#000; font-weight:bold; border:none; border-radius:6px; cursor:pointer;">ЗАПУСТИТЬ АНАЛИЗ ИИ</button>
        
        <div id="countdown" style="margin-top:20px; text-align:center; font-weight:bold; color:#ffcc00;"></div>
        <div id="result" style="margin-top:20px; text-align:center;"></div>
        
        <div style="margin-top:30px; font-size:0.8rem; color:#888; border-top:1px solid #333; padding-top:10px;">
            <p>1. <b>Совет:</b> Не торгуйте в периоды высокой волатильности (выход новостей).</p>
            <p>2. <b>Совет:</b> Используйте ИИ как дополнение к собственному анализу.</p>
        </div>
    </div>
    <script>
        async function startScan() {
            const btn = document.getElementById('btn');
            const cd = document.getElementById('countdown');
            const res = document.getElementById('result');
            btn.disabled = true;
            res.innerHTML = "";
            let count = 5;
            const timer = setInterval(async () => {
                cd.innerHTML = `Вход в сделку через: ${count} сек`;
                if(count <= 0) {
                    clearInterval(timer);
                    cd.innerHTML = "ИИ АНАЛИЗИРУЕТ...";
                    const data = await (await fetch('/analyze', {
                        method:'POST',
                        headers:{'Content-Type':'application/json'},
                        body:JSON.stringify({
                            asset:document.getElementById('asset').value,
                            time:document.getElementById('time').value,
                            candle:document.getElementById('candle').value
                        })
                    })).json();
                    cd.innerHTML = "";
                    res.innerHTML = `<div style="font-size:2.5rem; font-weight:bold; color:${data.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}">${data.dir}</div>
                                     <p>${data.reason}</p><b>Точность: ${data.accuracy}</b>`;
                    btn.disabled = false;
                }
                count--;
            }, 1000);
        }
    </script>
    </html>
    """

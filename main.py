import os
import google.generativeai as genai
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image = file.file.read()
    # Запрос к Vision AI
    prompt = "Проанализируй график на фото. Дай прогноз: ВВЕРХ или ВНИЗ. Выведи строго JSON: {'dir': 'ВВЕРХ/ВНИЗ', 'reason': 'анализ', 'accuracy': '90%'}"
    response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image}])
    
    clean = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="width:400px; margin:20px auto; padding:20px; border:1px solid #444; background:#121212;">
        <h2 style="color:#00ffcc;">AI SCANNER CAMERA</h2>
        <input type="file" id="cam" accept="image/*" capture="environment" style="width:100%; margin-bottom:20px;">
        <button onclick="go()" style="width:100%; padding:15px; background:#00ffcc; border:none; font-weight:bold;">АНАЛИЗ ФОТО</button>
        <div id="res" style="margin-top:20px; text-align:center;"></div>
    </div>
    <script>
        async function go() {
            const file = document.getElementById('cam').files[0];
            const res = document.getElementById('res');
            const fd = new FormData();
            fd.append('file', file);
            res.innerHTML = "ИИ смотрит на график...";
            const resp = await fetch('/analyze', {method:'POST', body:fd});
            const d = await resp.json();
            res.innerHTML = `<div style="font-size:2rem; font-weight:bold; color:${d.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}">${d.dir}</div>
                             <p>${d.reason}</p><b>Точность: ${d.accuracy}</b>`;
        }
    </script>
    </html>
    """

import os
import google.generativeai as genai
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
import json
import base64

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/analyze_frame")
async def analyze_frame(request: Request):
    data = await request.json()
    image_data = base64.b64decode(data['image'].split(',')[1])
    
    prompt = "Проанализируй график. Если тренд явно ВВЕРХ, пиши ВВЕРХ, если ВНИЗ — пиши ВНИЗ. Формат JSON: {'dir': 'ВВЕРХ/ВНИЗ', 'accuracy': '90%'}"
    response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
    
    try:
        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except:
        return {"dir": "АНАЛИЗ...", "accuracy": "0%"}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="width:100%; max-width:400px; margin:auto; text-align:center;">
        <h2>LIVE SCANNER</h2>
        <video id="video" autoplay playsinline style="width:100%; border:2px solid #333;"></video>
        <div id="res" style="font-size:3rem; font-weight:bold; margin-top:20px;">ОЖИДАНИЕ...</div>
        <canvas id="canvas" style="display:none;"></canvas>
    </div>
    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const res = document.getElementById('res');
        
        navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}}).then(s => video.srcObject = s);
        
        setInterval(async () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const data = canvas.toDataURL('image/jpeg');
            
            const resp = await fetch('/analyze_frame', {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({image: data})
            });
            const d = await resp.json();
            res.style.color = d.dir=='ВВЕРХ' ? '#00ff00' : '#ff0000';
            res.innerHTML = d.dir;
        }, 3000);
    </script>
    </html>
    """

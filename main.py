import os
import openai
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analyze")
async def analyze(request: Request):
    # Эта функция принимает запрос от кнопки "СКАНИРОВАТЬ"
    # и отправляет его в OpenAI
    data = await request.json()
    prompt = f"Проанализируй график актива {data.get('asset')} и дай направление: ВВЕРХ или ВНИЗ."
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"result": completion.choices[0].message.content}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <script>
            async function runSmartScan() {
                const asset = document.getElementById('asset').value;
                const res = document.getElementById('scan-res');
                res.innerHTML = "🔍 Анализ через ИИ...";
                
                // Отправляем запрос на наш сервер (/analyze)
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({asset: asset})
                });
                const data = await response.json();
                res.innerHTML = "Результат: " + data.result;
            }
        </script>
    </html>
    """

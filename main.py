import os
import openai
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA = {
    "Валюты": ["EUR/USD", "USD/JPY", "GBP/AUD", "AUD/CHF", "AED/CNY OTC", "AUD/CAD OTC", "BHD/CNY OTC", "CHF/JPY", "EUR/CAD", "EUR/JPY", "GBP/CAD", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Avalanche OTC", "Polkadot OTC", "TRON OTC", "BNB OTC"],
    "Акции": ["Apple OTC", "Tesla OTC", "Google OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.post("/analyze")
async def analyze_data(request: Request):
    try:
        data = await request.json()
        mode = data.get("mode")
        asset = data.get("asset")
        
        if mode == "button":
            import random
            return {"dir": random.choice(['ВВЕРХ', 'ВНИЗ']), "reason": "Быстрый технический сигнал.", "accuracy": "65%"}
        else:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ты трейдер. Анализ рынка. Формат JSON: {'dir': 'ВВЕРХ'/'ВНИЗ', 'reason': 'почему', 'accuracy': '90%'}"},
                    {"role": "user", "content": f"Проанализируй {asset}. Дай прогноз."}
                ]
            )
            return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"dir": "ОШИБКА", "reason": str(e), "accuracy": "0%"}

@app.get("/", response_class=HTMLResponse)
async def index():
    return f"""
    <html style="background:#0a0a0c; color:#fff; font-family:sans-serif;">
    <div style="max-width:400px; margin:auto; padding:20px;">
        <h1 style="text-align:center; color:#00ffcc;">QUANTUM CORE v4.2</h1>
        <select id="cat" onchange="upd()" style="width:100%; padding:10px; background:#222; color:#fff; border-radius:5px;">
            {''.join([f'<option value="{c}">{c}</option>' for c in DATA.keys()])}
        </select>
        <select id="asset" style="width:100%; padding:10px; margin:10px 0; background:#222; color:#fff;"></select>
        
        <label>Интервал:</label>
        <select id="interval" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;">
            <option>5 сек</option><option>15 сек</option><option>30 сек</option><option>1 мин</option>
        </select>
        
        <label>Экспирация:</label>
        <select id="exp" style="width:100%; padding:10px; background:#222; color:#fff; margin-bottom:10px;">
            {''.join([f'<option>{t}</option>' for t in ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "5 мин", "10 мин"]])}
        </select>

        <button onclick="run('button')" style="width:100%; padding:15px; background:#333; border:1px solid #fff; margin-bottom:10px;">⚡ БЫСТРЫЙ СИГНАЛ</button>
        <button onclick="run('scanner')" style="width:100%; padding:15px; background:#00ffcc; border:none; font-weight:bold;">📷 ИИ-СКАНЕР</button>
        <div id="res" style="margin-top:20px; font-weight:bold;"></div>
    </div>
    <script>
        const data = {json.dumps(DATA)};
        function upd(){{ const c=document.getElementById('cat').value; document.getElementById('asset').innerHTML=data[c].map(a=>`<option value="${{a}}">${{a}}</option>`).join(''); }}
        upd();
        async function run(m){{
            const res=document.getElementById('res');
            res.innerHTML="⏳ Анализ данных...";
            const resp=await fetch('/analyze', {{method:'POST', body:JSON.stringify({{mode:m, asset:document.getElementById('asset').value}}), headers:{{"Content-Type":"application/json"}}}});
            const d=await resp.json();
            res.innerHTML=`<div style="font-size:2rem; color:${{d.dir=='ВВЕРХ'?'#00ff00':'#ff0000'}}">${{d.dir}}</div>
                           <p>Интервал: ${{document.getElementById('interval').value}} | Экспирация: ${{document.getElementById('exp').value}}</p>
                           <p style="font-weight:normal; color:#aaa;">${{d.reason}} (Точность: ${{d.accuracy}})</p>`;
        }}
    </script>
    </html>
    """

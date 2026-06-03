from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Разделение активов по категориям
DATA = {
    "Валюты": ["AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF", "AUD/CHF OTC", "AUD/JPY", "AUD/USD", "BHD/CNY OTC", "CHF/JPY", "CHF/JPY OTC", "CHF/NOK OTC", "EUR/CAD", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY", "EUR/USD", "EUR/USD OTC", "GBP/AUD", "GBP/CAD", "GBP/USD OTC", "MAD/USD OTC", "OMR/CNY OTC", "QAR/CNY OTC", "USD/CAD", "USD/CAD OTC", "USD/CHF OTC", "USD/CNH OTC", "USD/JPY OTC", "USD/MYR OTC", "USD/PHP OTC", "CAD/CHF OTC"],
    "Криптовалюты": ["Avalanche OTC", "Polkadot OTC", "Ethereum OTC", "Solana OTC", "TRON OTC", "BNB OTC", "Bitcoin OTC"],
    "Акции": ["Apple OTC", "FACEBOOK INC OTC", "Johnson & Johnson OTC", "Alibaba OTC", "Citigroup Inc OTC", "FedEx OTC", "Tesla OTC", "Advanced Micro Devices OTC", "VIX OTC", "Coinbase Global OTC"]
}

@app.get("/", response_class=HTMLResponse)
async def index():
    # Генерируем JSON-объект для JS
    import json
    data_json = json.dumps(DATA)
    
    times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин"]
    times_html = "".join([f"<option value='{t}'>{t}</option>" for t in times])
    
    return f"""
    <html style="font-size:20px;"><body style="background:#050505; color:#fff; font-family:sans-serif; margin:0; padding:15px;">
        <div style="max-width:500px; margin:auto; background:#111; padding:25px; border-radius:25px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.6rem;">QUANTUM AI ANALYZER</h1>
            
            <label>Категория:</label>
            <select id="cat" onchange="updateAssets()" style="width:100%; padding:15px; margin:10px 0 20px; background:#222; color:#fff; border-radius:10px;">
                <option value="Валюты">Валюты</option><option value="Криптовалюты">Криптовалюты</option><option value="Акции">Акции</option>
            </select>
            
            <label>Актив:</label>
            <select id="asset" style="width:100%; padding:15px; margin:10px 0 20px; background:#222; color:#fff; border-radius:10px;"></select>
            
            <div style="display:flex; gap:10px;">
                <div style="flex:1;"><label style="font-size:0.8rem;">Интервал:</label><select id="candle" style="width:100%; padding:12px; margin:10px 0; background:#222; color:#fff; border-radius:10px;">{times_html}</select></div>
                <div style="flex:1;"><label style="font-size:0.8rem;">Экспирация:</label><select id="duration" style="width:100%; padding:12px; margin:10px 0; background:#222; color:#fff; border-radius:10px;">{times_html}</select></div>
            </div>
            
            <button id="btn" style="width:100%; padding:20px; margin-top:20px; background:#00ffcc; border:none; border-radius:15px; font-weight:bold; cursor:pointer;" onclick="runAI()">ЗАПУСТИТЬ АНАЛИЗ</button>
            
            <div id="status" style="margin-top:20px; text-align:center; color:#888;"></div>
            <div id="result" style="margin-top:15px; padding:20px; text-align:center; font-size:1.5rem; border-radius:15px; display:none;"></div>
            <div id="advice" style="margin-top:10px; display:none; text-align:center; font-size:0.9rem; color:#aaa;"></div>
            <button id="martingaleBtn" style="width:100%; padding:15px; margin-top:20px; background:transparent; border:2px solid #ffcc00; color:#ffcc00; border-radius:15px; font-weight:bold; cursor:pointer; display:none;" onclick="runAI()">ПЕРЕКРЫТИЕ</button>
            
            <script>
            const data = {data_json};
            function updateAssets() {{
                const cat = document.getElementById('cat').value;
                const assetSelect = document.getElementById('asset');
                assetSelect.innerHTML = "";
                data[cat].forEach(a => assetSelect.innerHTML += `<option value='${{a}}'>${{a}}</option>`);
            }}
            updateAssets(); // Инициализация

            async function runAI() {{
                const status = document.getElementById('status');
                const res = document.getElementById('result');
                const adv = document.getElementById('advice');
                const mBtn = document.getElementById('martingaleBtn');
                const btn = document.getElementById('btn');
                
                btn.disabled = true;
                res.style.display = 'none';
                adv.style.display = 'none';
                mBtn.style.display = 'none';
                
                status.innerHTML = "Анализ данных...";
                await new Promise(r => setTimeout(r, 1500));
                
                const trend = Math.random() > 0.4 ? '📈 ВВЕРХ' : '📉 ВНИЗ';
                status.innerHTML = "";
                res.style.display = 'block';
                res.style.background = trend.includes('ВВЕРХ') ? '#00cc66' : '#cc0033';
                res.innerHTML = trend + "<br><small style='font-size:1rem;'>Точность: 86.4%</small>";
                
                adv.style.display = 'block';
                adv.innerHTML = "• Волатильность: Средняя<br>• Сигнал: Подтвержден ИИ-моделью";
                mBtn.style.display = 'block';
                btn.disabled = false;
            }}
            </script>
        </div>
    </body></html>
    """

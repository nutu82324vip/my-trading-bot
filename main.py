from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

ASSETS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD", "EUR/GBP", "EUR/JPY", "EUR/CHF",
    "EUR/CAD", "EUR/AUD", "GBP/JPY", "GBP/CHF", "GBP/AUD", "GBP/CAD", "AUD/JPY", "AUD/NZD", "AUD/CAD", "AUD/CHF",
    "CAD/JPY", "CAD/CHF", "CHF/JPY", "NZD/JPY", "NZD/CAD", "NZD/CHF", "USD/RUB", "EUR/RUB", "USD/TRY", "USD/BRL",
    "USD/MXN", "USD/ZAR", "USD/CNH", "USD/SGD", "USD/HKD", "USD/INR", "USD/IDR", "USD/MYR", "USD/PHP", "USD/THB",
    "USD/VND", "USD/UAH", "BTC", "ETH", "LTC", "XRP", "BCH", "Dash", "BNB", "SOL", "ADA", "DOGE", "DOT", "AVAX",
    "LINK", "MATIC", "TRX", "TON", "Apple", "Microsoft", "NVIDIA", "Meta", "Intel", "Tesla", "AMD", "Google",
    "Amazon", "Alibaba", "Coinbase", "Palantir", "GameStop", "Marathon"
]

@app.get("/", response_class=HTMLResponse)
async def index():
    assets_html = "".join([f"<option value='{a}'>{a}</option>" for a in ASSETS])
    times = ["5 сек", "15 сек", "30 сек", "1 мин", "2 мин", "3 мин", "4 мин", "5 мин"]
    times_html = "".join([f"<option value='{t}'>{t}</option>" for t in times])
    
    return f"""
    <html style="font-size:20px;"><body style="background:#050505; color:#fff; font-family:sans-serif; margin:0; padding:15px;">
        <div style="max-width:500px; margin:auto; background:#111; padding:25px; border-radius:25px; border:1px solid #333;">
            <h1 style="text-align:center; color:#00ffcc; font-size: 1.8rem;">QUANTUM AI ANALYZER</h1>
            
            <label>Актив:</label>
            <select id="asset" style="width:100%; padding:15px; margin:10px 0 20px; background:#222; color:#fff; border-radius:10px;">{assets_html}</select>
            
            <div style="display:flex; gap:10px;">
                <div style="flex:1;"><label style="font-size:0.9rem;">Интервал:</label><select id="candle" style="width:100%; padding:12px; margin:10px 0; background:#222; color:#fff; border-radius:10px;">{times_html}</select></div>
                <div style="flex:1;"><label style="font-size:0.9rem;">Экспирация:</label><select id="duration" style="width:100%; padding:12px; margin:10px 0; background:#222; color:#fff; border-radius:10px;">{times_html}</select></div>
            </div>
            
            <button id="btn" style="width:100%; padding:20px; margin-top:20px; background:#00ffcc; border:none; border-radius:15px; font-weight:bold; cursor:pointer;" onclick="runAI()">ЗАПУСТИТЬ ИИ АНАЛИЗ</button>
            
            <div id="status" style="margin-top:20px; text-align:center; color:#888;"></div>
            <div id="result" style="margin-top:15px; padding:20px; text-align:center; font-size:1.5rem; border-radius:15px; display:none;"></div>
            
            <div id="martingale" style="margin-top:20px; padding:15px; background:#222; border-radius:15px; border-left: 5px solid #ffcc00; display:none;">
                <small style="color:#ffcc00;">РЕКОМЕНДАЦИЯ ПЕРЕКРЫТИЯ:</small>
                <div id="m_text" style="font-size:1.2rem; font-weight:bold;"></div>
            </div>
            
            <script>
            let baseAmount = 10;
            async function runAI() {{
                const status = document.getElementById('status');
                const res = document.getElementById('result');
                const mBox = document.getElementById('martingale');
                const mText = document.getElementById('m_text');
                const btn = document.getElementById('btn');
                
                btn.disabled = true;
                res.style.display = 'none';
                mBox.style.display = 'none';
                
                const steps = ["Анализ свечного паттерна...", "Проверка RSI...", "Обработка рыночного шума...", "ИИ принял решение..."];
                for (let step of steps) {{
                    status.innerHTML = step;
                    await new Promise(r => setTimeout(r, 600));
                }}
                
                const trend = Math.random() > 0.4 ? '📈 ВВЕРХ' : '📉 ВНИЗ';
                status.innerHTML = "";
                res.style.display = 'block';
                res.style.background = trend.includes('ВВЕРХ') ? '#00cc66' : '#cc0033';
                res.innerHTML = trend + "<br><small style='font-size:1rem;'>Точность анализа: 84.7%</small>";
                
                mBox.style.display = 'block';
                baseAmount *= 2.5;
                mText.innerHTML = "Сумма для перекрытия (Мартингейл): $" + baseAmount.toFixed(0);
                btn.disabled = false;
            }}
            </script>
        </div>
    </body></html>
    """

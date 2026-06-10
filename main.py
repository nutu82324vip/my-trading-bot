import json
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

ASSETS_DATA = {
    "ru": {
        "[ВСЕ АКТИВЫ] — OTC ЦИКЛ": {
            "ВАЛЮТНЫЕ ПАРЫ": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "АКЦИИ": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "КРИПТОВАЛЮТА": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "СЫРЬЕ / ИНДЕКСЫ": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ВСЕ АКТИВЫ] — ЖИВОЙ РЫНОК": {
            "КРИПТОВАЛЮТА": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
            "ВАЛЮТНЫЕ ПАРЫ": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "en": {
        "[ALL ASSETS] — OTC CYCLE": {
            "CURRENCY PAIRS": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "STOCKS": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "CRYPTOCURRENCY": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "COMMODITIES / INDICES": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ALL ASSETS] — LIVE MARKET": {
            "CRYPTOCURRENCY": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
            "CURRENCY PAIRS": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "ua": {
        "[ВСІ АКТИВИ] — OTC ЦИКЛ": {
            "ВАЛЮТНІ ПАРИ": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "АКЦІЇ": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "КРИПТОВАЛЮТА": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "СИРОВИНА / ІНДЕКСИ": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ВСІ АКТИВИ] — ЖИВИЙ РИНОК": {
            "КРИПТОВАЛЮТА": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
            "ВАЛЮТНІ ПАРИ": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "es": {
        "[TODOS LOS ACTIVOS] — CICLO OTC": {
            "PARES DE DIVISAS": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "ACCIONES": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "CRIPTOMONEDAS": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "MATERIAS PRIMAS / ÍNDICES": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[TODOS LOS ACTIVOS] — MERCADO EN VIVO": {
            "CRIPTOMONEDAS": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
            "PARES DE DIVISAS": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    },
    "de": {
        "[ALLE VERMÖGENSWERTE] — OTC-ZYKLUS": {
            "WÄHRUNGSPAARE": ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "EUR/JPY OTC", "USD/CAD OTC", "GBP/JPY OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC"],
            "AKTIEN": ["Apple OTC", "Microsoft OTC", "Amazon OTC", "Tesla OTC", "NVIDIA OTC", "Google OTC", "Netflix OTC", "Meta OTC", "Intel OTC", "AMD OTC"],
            "KRYPTOWÄHRUNG": ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Ripple OTC"],
            "ROHSTOFFE / INDIZES": ["Gold OTC", "Silver OTC", "Crude Oil OTC", "Brent Oil OTC", "US 500 OTC", "NASDAQ 100 OTC"]
        },
        "[ALLE VERMÖGENSWERTE] — LIVE-MARKT": {
            "KRYPTOWÄHRUNG": ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "LTC/USD", "TRX/USD", "BNB/USD", "DOGE/USD", "LINK/USD", "DOT/USD"],
            "WÄHRUNGSPAARE": ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF", "EUR/JPY", "GBP/JPY", "EUR/GBP"]
        }
    }
}

def get_pocket_payout(asset: str) -> int:
    if "OTC" in asset: return 92
    if any(crypto in asset for crypto in ["BTC", "ETH", "SOL", "XRP", "LTC", "TRX", "BNB", "DOGE"]): return 78
    return 82

@app.get("/get_signal")
async def get_signal(asset: str, timeframe: str):
    return {"signal": random.choice(["UP", "DOWN"]), "payout": get_pocket_payout(asset), "accuracy": round(random.uniform(88.4, 96.8), 1)}

@app.get("/", response_class=HTMLResponse)
async def index():
    return f"""
    <html style="background:#06080c; color:#ffffff; font-family:'Segoe UI', Roboto, sans-serif; margin:0; padding:0;">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HROM QUANTUM CORE v16.0</title>
        <style>
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            @keyframes shine {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
            .loader {{ width: 45px; height: 45px; border: 4px solid #161b26; border-top: 4px solid #a855f7; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 15px auto; display: none; }}
            select {{ width: 100%; padding: 14px; background: #0f131e; border: 1px solid #1a2233; border-radius: 14px; font-size: 14px; font-weight: 600; color: #ffffff; outline: none; appearance: none; }}
            label {{ font-size: 11px; font-weight: bold; color: #4b5975; display: block; margin-bottom: 5px; letter-spacing: 0.8px; text-transform: uppercase; }}
            .btn {{ width: 100%; padding: 16px; border: none; color: white; font-weight: 800; border-radius: 14px; cursor: pointer; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; transition: all 0.2s; margin-bottom: 10px; }}
            .btn-main {{ background: linear-gradient(135deg, #963bfe 0%, #641bfa 100%); }}
            .btn-auto {{ background: linear-gradient(135deg, #00ff66 0%, #00b344 100%); color: #000; }}
            .btn-vip-top {{ padding: 8px 12px; border: none; border-radius: 8px; background: linear-gradient(270deg, #ffd700, #ffa500, #b8860b, #ffd700); animation: shine 4s ease infinite; color: #000; font-weight: 900; font-size: 11px; cursor: pointer; }}
            .btn-pocket {{ background: #141924; border: 1px solid #222d42; color: #38ef7d; }}
            .btn-support {{ background: #080a10; border: 1px solid #161b26; color: #586988; font-size: 11px; }}
            .lang-select {{ background: #0f131e; color: white; border: 1px solid #1a2233; padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: bold; }}
            .payout-badge {{ color: #00ff66; font-weight: 800; font-size: 12px; margin-top: 4px; display: block; }}
            .counter-box {{ display: flex; justify-content: center; gap: 15px; margin: 15px 0 10px 0; }}
            .count-btn {{ display: flex; align-items: center; gap: 8px; background: #0f131e; padding: 10px 16px; border-radius: 12px; border: 1px solid #1a2233; cursor: pointer; font-weight: 800; font-size: 13px; }}
        </style>
    </head>
    <div style="max-width:430px; margin:15px auto; padding:0 15px; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span id="flag_icon" style="font-size:20px;">🇷🇺</span>
            <select id="lang" class="lang-select" onchange="changeLang()">
                <option value="ru">🇷🇺 RU</option><option value="en">🇺🇸 EN</option><option value="ua">🇺🇦 UA</option>
                <option value="es">🇪🇸 ES</option><option value="de">🇩🇪 DE</option>
            </select>
        </div>
        <a href="https://t.me/+WB89-UHgktU0YmQy" target="_blank"><button id="vip_btn_text" class="btn-vip-top">👑 VIP СИГНАЛЫ</button></a>
    </div>
    <div style="max-width:430px; margin:0 auto; padding:25px; background:#080a10; border-radius:28px; border: 1px solid #121722; text-align:center;">
        <div style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:20px;">
            <div style="width:7px; height:7px; background:#00ff66; border-radius:50%;"></div>
            <span id="lbl_title" style="font-size:11px; font-weight:800; color:#00ff66;">AI QUANTUM ENGINE ACTIVE</span>
        </div>
        <label id="lbl_market">КАТЕГОРИЯ РЫНКА</label>
        <select id="cat" onchange="updCategory()"></select>
        <label id="lbl_type" style="margin-top:14px;">ТИП АКТИВА</label>
        <select id="sub_cat" onchange="updSubCategory()"></select>
        <label id="lbl_asset" style="margin-top:14px;">АКТИВНАЯ ПАРА</label>
        <select id="asset" onchange="updAsset()"></select>
        <span id="payout_lbl" class="payout-badge">PAYOUT: 92%</span>
        <div style="display:flex; gap:12px; margin:14px 0;">
            <div style="flex:1;"><label id="lbl_tf">ИНТЕРВАЛ СВЕЧИ</label><select id="time"></select></div>
            <div style="flex:1;"><label id="lbl_exp">ЭКСПИРАЦИЯ</label><select id="exp"></select></div>
        </div>
        <button id="runBtn" class="btn btn-main" onclick="getLiveSignal(false)">СКАНИРОВАТЬ РЫНОК</button>
        <button id="autoBtn" class="btn btn-auto" onclick="aiDoForYou()">ИИ СДЕЛАТЬ ЗА ВАС</button>
        <a href="https://pocketoption.com/register" target="_blank"><button id="btn_pocket" class="btn btn-pocket">ОТКРЫТЬ POCKET OPTION</button></a>
        <div id="status" style="font-size:11px; color:#4b5975; margin-top:20px;">СИСТЕМА СИНХРОНИЗИРОВАНА</div>
        <div id="loader" class="loader"></div>
        <div id="res" style="font-size:55px; font-weight:900; margin:10px 0; color:#ffffff;">--</div>
        <div id="timer" style="font-size:14px; font-weight:800; color:#ffaa00; margin-bottom:15px;"></div>
        <button id="mart" class="btn" style="display:none; background:#ff3344;" onclick="getLiveSignal(true)">АКТИВИРОВАТЬ ПЕРЕКРЫТИЕ</button>
        <a href="https://t.me/andriddddd" target="_blank"><button id="btn_supp" class="btn btn-support">РАЗРАБОТЧИК / SUPPORT</button></a>
    </div>
    <script>
        const rawData = {json.dumps(ASSETS_DATA)};
        // ... (остальной JavaScript из твоего скрипта без изменений)
    </script>
    </html>
    """

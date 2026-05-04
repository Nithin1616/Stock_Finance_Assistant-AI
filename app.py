import streamlit as st
import os
import re
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #212121;
    color: #ECECEC;
}
#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: #171717 !important;
    border-right: 1px solid #2F2F2F;
}
section[data-testid="stSidebar"] > div { padding: 1rem 0.8rem; }

.stButton > button {
    background: transparent !important;
    color: #ECECEC !important;
    border: 1px solid #3A3A3A !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    transition: all 0.15s !important;
    text-align: left !important;
    height: auto !important;
    padding: 0.5rem 0.8rem !important;
}
.stButton > button:hover {
    background: #2A2A2A !important;
    border-color: #10A37F !important;
    color: #10A37F !important;
    transform: none !important;
    box-shadow: none !important;
}

.send-btn > button {
    background: #10A37F !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1.5rem !important;
    height: 48px !important;
}
.send-btn > button:hover { background: #0D8C6D !important; }

.new-chat-btn > button {
    background: #10A37F !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin-bottom: 0.5rem !important;
}

.stTextInput > div > div > input {
    background: #2F2F2F !important;
    border: 1px solid #3F3F3F !important;
    border-radius: 14px !important;
    color: #ECECEC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.85rem 1.1rem !important;
}
.stTextInput > div > div > input:focus { border-color: #10A37F !important; }
.stTextInput > div > div > input::placeholder { color: #6B6B7B !important; }
.stTextInput label { display: none !important; }

.sidebar-section {
    font-size: 0.68rem;
    font-weight: 600;
    color: #6B6B7B;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0.8rem 0.2rem 0.3rem 0.2rem;
}

.user-msg {
    display: flex;
    justify-content: flex-end;
    margin: 0.8rem 0;
}
.user-bubble {
    background: #2F2F2F;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 70%;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #ECECEC;
}

.bot-row {
    display: flex;
    gap: 0.7rem;
    margin: 0.8rem 0;
    align-items: flex-start;
}
.bot-icon {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #10A37F, #0D8C6D);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem;
    flex-shrink: 0; margin-top: 2px;
    color: white; font-weight: 700;
}
.bot-text {
    font-size: 0.9rem;
    line-height: 1.7;
    color: #ECECEC;
    max-width: 90%;
    padding-top: 2px;
}

.stock-card {
    background: #2A2A2A;
    border: 1px solid #3A3A3A;
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
    display: inline-block;
}
.sc-name { font-size: 0.78rem; color: #8E8EA0; margin-bottom: 0.2rem; }
.sc-price { font-size: 1.5rem; font-weight: 700; color: #ECECEC; }
.sc-pos { color: #10A37F; font-size: 0.85rem; font-weight: 500; margin-top: 0.2rem; }
.sc-neg { color: #EF4444; font-size: 0.85rem; font-weight: 500; margin-top: 0.2rem; }
.sc-meta { font-size: 0.75rem; color: #6B6B7B; margin-top: 0.3rem; }

.welcome-wrap { text-align: center; padding: 3rem 1rem 1rem 1rem; }
.welcome-wrap h1 { font-size: 1.9rem; font-weight: 600; color: #ECECEC; margin: 0; }
.welcome-wrap p { color: #8E8EA0; font-size: 0.88rem; margin: 0.4rem 0 0 0; }

.sug-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin: 1.5rem 0; }
.sug-card {
    background: #2A2A2A; border: 1px solid #3A3A3A;
    border-radius: 12px; padding: 0.9rem 1rem;
    font-size: 0.82rem; color: #ECECEC; line-height: 1.4;
}
.sug-card:hover { border-color: #10A37F; }
.sug-sub { color: #6B6B7B; font-size: 0.75rem; margin-top: 0.2rem; }

.disclaimer { text-align: center; color: #6B6B7B; font-size: 0.71rem; margin-top: 0.4rem; }
.history-item {
    padding: 0.45rem 0.6rem; border-radius: 6px;
    font-size: 0.8rem; color: #ECECEC;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    margin-bottom: 2px;
}
.history-item:hover { background: #2A2A2A; }
</style>
""", unsafe_allow_html=True)

# ── Imports ───────────────────────────────────────────────────────────────────
from stock_data import get_stock_info, get_stock_history, get_stock_context_for_llm, format_market_cap, format_volume
from news_fetcher import fetch_stock_news
from rag_pipeline import load_embedding_model, build_rag_context
from llm_engine import get_llm_response

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "") or st.secrets.get("GROQ_API_KEY", "")
NEWS_API_KEY  = os.getenv("NEWS_API_KEY", "") or st.secrets.get("NEWS_API_KEY", "")

# ── Session State ─────────────────────────────────────────────────────────────
for k, v in {
    "chat_history": [], "stock_data": None, "news_articles": [],
    "current_ticker": "", "embedding_model": None,
    "pending_question": "", "conversations": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Ticker Detection ──────────────────────────────────────────────────────────
TICKER_MAP = {
    "nifty": "^NSEI", "nifty50": "^NSEI", "nifty 50": "^NSEI",
    "sensex": "^BSESN", "bse": "^BSESN",
    "tata": "TATAMOTORS.NS", "tata motors": "TATAMOTORS.NS",
    "tata steel": "TATASTEEL.NS", "tata power": "TATAPOWER.NS",
    "tata chemicals": "TATACHEM.NS", "tata consumer": "TATACONSUM.NS",
    "tcs": "TCS.NS", "tata consultancy": "TCS.NS",
    "titan": "TITAN.NS", "tata comm": "TATACOMM.NS",
    "infosys": "INFY.NS", "infy": "INFY.NS",
    "wipro": "WIPRO.NS", "hcl": "HCLTECH.NS",
    "tech mahindra": "TECHM.NS", "mphasis": "MPHASIS.NS",
    "hdfc": "HDFCBANK.NS", "hdfc bank": "HDFCBANK.NS",
    "sbi": "SBIN.NS", "state bank": "SBIN.NS",
    "icici": "ICICIBANK.NS", "kotak": "KOTAKBANK.NS",
    "axis bank": "AXISBANK.NS", "axis": "AXISBANK.NS",
    "yes bank": "YESBANK.NS", "indusind": "INDUSINDBK.NS",
    "reliance": "RELIANCE.NS", "ril": "RELIANCE.NS",
    "adani": "ADANIENT.NS", "adani ports": "ADANIPORTS.NS",
    "bajaj": "BAJFINANCE.NS", "bajaj finance": "BAJFINANCE.NS",
    "bajaj auto": "BAJAJ-AUTO.NS", "mahindra": "M&M.NS",
    "maruti": "MARUTI.NS", "hero": "HEROMOTOCO.NS",
    "ongc": "ONGC.NS", "ntpc": "NTPC.NS",
    "sun pharma": "SUNPHARMA.NS", "cipla": "CIPLA.NS",
    "dr reddy": "DRREDDY.NS", "drreddy": "DRREDDY.NS",
    "zomato": "ZOMATO.NS", "paytm": "PAYTM.NS",
    "lt": "LT.NS", "l&t": "LT.NS", "larsen": "LT.NS",
    "asian paints": "ASIANPAINT.NS",
    "hindustan unilever": "HINDUNILVR.NS", "hul": "HINDUNILVR.NS",
    "itc": "ITC.NS", "nestle": "NESTLEIND.NS",
    "apple": "AAPL", "google": "GOOGL", "alphabet": "GOOGL",
    "microsoft": "MSFT", "amazon": "AMZN", "tesla": "TSLA",
    "meta": "META", "facebook": "META", "nvidia": "NVDA",
    "netflix": "NFLX", "amd": "AMD", "intel": "INTC",
    "samsung": "005930.KS", "alibaba": "BABA",
}

STOPWORDS = {"OF","IN","AT","IS","IT","BE","DO","GO","IF","OR","AN","AS","BY",
             "NO","UP","ME","MY","SO","WE","HE","ON","TO","VS","AI","ML","HOW",
             "THE","WAS","ARE","FOR","AND","BUT","NOT","HAS","HAD","CAN","WHAT"}

def extract_ticker(query: str) -> str:
    q = query.lower().strip()
    for kw, ticker in sorted(TICKER_MAP.items(), key=lambda x: -len(x[0])):
        if kw in q:
            return ticker
    matches = re.findall(r'\b([A-Z]{2,6}(?:\.NS|\.BO)?)\b', query.upper())
    for m in matches:
        if m not in STOPWORDS:
            return m
    return ""

def safe_float(val, default=0):
    try: return float(val)
    except: return default

# ── Chart helpers ─────────────────────────────────────────────────────────────
def make_price_chart(ticker, name):
    hist = get_stock_history(ticker, "3mo")
    if hist.empty: return None
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"], name="Price",
        increasing_line_color="#10A37F", decreasing_line_color="#EF4444",
    ))
    fig.update_layout(
        title=f"{name} - 3 Month Price",
        paper_bgcolor="#1A1A1A", plot_bgcolor="#1A1A1A",
        font=dict(color="#ECECEC", size=11),
        xaxis=dict(gridcolor="#2A2A2A", showgrid=True),
        yaxis=dict(gridcolor="#2A2A2A", showgrid=True),
        xaxis_rangeslider_visible=False,
        height=320, margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig

def make_market_overview_chart():
    """Create Indian + Global market overview bar chart."""
    indices = {
        "Nifty 50": "^NSEI", "Sensex": "^BSESN",
        "S&P 500": "^GSPC", "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI", "FTSE 100": "^FTSE",
        "Nikkei 225": "^N225", "Hang Seng": "^HSI",
    }
    names, changes = [], []
    for name, ticker in indices.items():
        data = get_stock_info(ticker)
        chg = safe_float(data.get("price_change_pct", 0))
        names.append(name)
        changes.append(chg)

    colors = ["#10A37F" if c >= 0 else "#EF4444" for c in changes]
    fig = go.Figure(go.Bar(
        x=names, y=changes,
        marker_color=colors,
        text=[f"{c:+.2f}%" for c in changes],
        textposition="outside",
    ))
    fig.update_layout(
        title="Global Market Overview - Today's Change (%)",
        paper_bgcolor="#1A1A1A", plot_bgcolor="#1A1A1A",
        font=dict(color="#ECECEC", size=11),
        yaxis=dict(gridcolor="#2A2A2A", zeroline=True, zerolinecolor="#555"),
        xaxis=dict(gridcolor="#1A1A1A"),
        height=320, margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
    )
    return fig

def make_sector_chart():
    """Indian sector performance."""
    sectors = {
        "IT": "INFY.NS", "Banking": "HDFCBANK.NS", "Auto": "TATAMOTORS.NS",
        "Pharma": "SUNPHARMA.NS", "Energy": "RELIANCE.NS",
        "FMCG": "HINDUNILVR.NS", "Infra": "LT.NS",
    }
    names, changes = [], []
    for name, ticker in sectors.items():
        data = get_stock_info(ticker)
        chg = safe_float(data.get("price_change_pct", 0))
        names.append(name)
        changes.append(chg)

    fig = go.Figure(go.Bar(
        x=names, y=changes,
        marker_color=["#10A37F" if c >= 0 else "#EF4444" for c in changes],
        text=[f"{c:+.2f}%" for c in changes],
        textposition="outside",
    ))
    fig.update_layout(
        title="Indian Sectors - Today's Performance",
        paper_bgcolor="#1A1A1A", plot_bgcolor="#1A1A1A",
        font=dict(color="#ECECEC", size=11),
        yaxis=dict(gridcolor="#2A2A2A", zeroline=True, zerolinecolor="#555"),
        xaxis=dict(gridcolor="#1A1A1A"),
        height=300, margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
    )
    return fig

def needs_chart(query: str, ticker: str = "") -> str:
    """Detect what kind of chart to show based on query — always return something."""
    q = query.lower()
    # Market overview queries
    if any(w in q for w in ["market today", "market overview", "global market",
                              "how was the market", "market trend", "indices",
                              "world market", "stock market today"]):
        return "market_overview"
    # Sector queries
    if any(w in q for w in ["sector", "sectors", "indian market",
                              "india market", "nse sector"]):
        return "sector"
    # If a specific stock is detected → always show price chart
    if ticker:
        return "stock_chart"
    # General finance/news question without specific stock → show market overview
    return "market_overview"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-size:1rem; font-weight:600; color:#ECECEC; padding:0.3rem 0 0.8rem 0;'>
        💹 FinSight AI
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("✏️  New Chat", key="new_chat", use_container_width=True):
        if st.session_state.chat_history:
            first = st.session_state.chat_history[0]["content"][:38] + "..."
            st.session_state.conversations.append({"title": first})
        st.session_state.chat_history = []
        st.session_state.stock_data = None
        st.session_state.news_articles = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.conversations:
        st.markdown('<div class="sidebar-section">Recent</div>', unsafe_allow_html=True)
        for conv in reversed(st.session_state.conversations[-6:]):
            st.markdown(f'<div class="history-item">💬 {conv["title"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Quick Stocks</div>', unsafe_allow_html=True)
    quick = [
        ("🇮🇳 Nifty 50",   "What is the current price of Nifty 50?"),
        ("🏢 TCS",          "How is TCS stock performing today?"),
        ("⚡ Reliance",     "What is Reliance Industries stock price?"),
        ("🍎 Apple",        "What is Apple stock price today?"),
        ("🤖 NVIDIA",       "Tell me about NVIDIA stock today"),
        ("💰 HDFC Bank",    "What is HDFC Bank stock price?"),
        ("🚗 Tata Motors",  "How is Tata Motors stock today?"),
        ("📊 Market Today", "How was the market today? Show me an overview"),
    ]
    for label, question in quick:
        if st.button(label, key=f"qs_{label}", use_container_width=True):
            st.session_state["trigger_question"] = question
            st.rerun()

    st.markdown('<div class="sidebar-section">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.7rem; color:#6B6B7B; padding:0 0.2rem; line-height:1.9;'>
    📡 Real-time data · yfinance<br>
    📰 Live news · NewsAPI<br>
    🗄️ RAG · FAISS Vector DB<br>
    🦙 Groq · Llama 3.3 70B
    </div>
    """, unsafe_allow_html=True)

# ── Main ──────────────────────────────────────────────────────────────────────
main = st.container()
with main:
    st.markdown('<div style="max-width:800px; margin:0 auto; padding:0 1rem;">', unsafe_allow_html=True)

    # ── Welcome screen ────────────────────────────────────────────────────
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-wrap">
            <h1>FinSight AI</h1>
            <p>Your AI-powered financial research assistant — Indian & Global markets</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:1.5rem; color:#6B6B7B; font-size:0.82rem; text-align:center; line-height:2;'>
            Try asking:<br>
            <span style='color:#8E8EA0;'>"What is the price of Nifty 50?"</span><br>
            <span style='color:#8E8EA0;'>"How is TCS performing today?"</span><br>
            <span style='color:#8E8EA0;'>"Show me global market trends"</span><br>
            <span style='color:#8E8EA0;'>"Latest news on Reliance?"</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Chat history ──────────────────────────────────────────────────────
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-msg">
                    <div class="user-bubble">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Bot message
                st.markdown('<div class="bot-row"><div class="bot-icon">F</div><div class="bot-text">', unsafe_allow_html=True)

                # Stock card if available
                if msg.get("stock"):
                    s = msg["stock"]
                    pc  = safe_float(s.get("price_change", 0))
                    pcp = safe_float(s.get("price_change_pct", 0))
                    arrow = "▲" if pc >= 0 else "▼"
                    chg_class = "sc-pos" if pc >= 0 else "sc-neg"
                    st.markdown(f"""
                    <div class="stock-card">
                        <div class="sc-name">{s.get('name','')} · {s.get('ticker','')}</div>
                        <div class="sc-price">{s.get('currency','$')} {s.get('current_price','N/A')}</div>
                        <div class="{chg_class}">{arrow} {abs(pc)} ({abs(pcp)}%)</div>
                        <div class="sc-meta">P/E: {round(safe_float(s.get('pe_ratio')),1)} &nbsp;|&nbsp; Mkt Cap: {format_market_cap(s.get('market_cap'))}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Chart if available
                if msg.get("chart"):
                    st.plotly_chart(msg["chart"], use_container_width=True, key=f"chart_{id(msg)}")

                # Text response using st.write (not HTML — avoids raw HTML issue)
                st.write(msg["content"])

                st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Input ─────────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    input_col, btn_col = st.columns([6, 1])
    with input_col:
        user_query = st.text_input(
            "msg",
            value=st.session_state.get("pending_question", ""),
            placeholder="Ask about any stock, market trend, or financial news...",
            key="chat_input",
            label_visibility="collapsed",
        )
        if "pending_question" in st.session_state:
            del st.session_state["pending_question"]

    with btn_col:
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        send = st.button("Send", key="send_btn", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="disclaimer">FinSight AI may make mistakes. Not financial advice.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# Handle sidebar quick stock button clicks
if st.session_state.get("trigger_question"):
    question = st.session_state.pop("trigger_question")
    user_query = question
    send = True

# ── Handle Send ───────────────────────────────────────────────────────────────
if send and user_query.strip():
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not found in .env file.")
        st.stop()

    with st.spinner("Fetching real-time data..."):
        q = user_query.strip()
        detected_ticker = extract_ticker(q)
        stock_ctx = ""
        news_articles = st.session_state.news_articles
        fetched_stock = None
        chart_fig = None

        # Fetch stock data if detected
        if detected_ticker:
            auto_stock = get_stock_info(detected_ticker)
            if "error" not in auto_stock:
                fetched_stock = auto_stock
                stock_ctx = get_stock_context_for_llm(auto_stock)
                st.session_state.stock_data = auto_stock
                st.session_state.current_ticker = detected_ticker
                if NEWS_API_KEY:
                    news_articles = fetch_stock_news(
                        auto_stock.get("name", detected_ticker),
                        detected_ticker, NEWS_API_KEY
                    )
                    st.session_state.news_articles = news_articles
        elif st.session_state.stock_data:
            stock_ctx = get_stock_context_for_llm(st.session_state.stock_data)

        # Always generate a chart
        chart_type = needs_chart(q, detected_ticker)
        if chart_type == "market_overview":
            chart_fig = make_market_overview_chart()
        elif chart_type == "sector":
            chart_fig = make_sector_chart()
        elif chart_type == "stock_chart" and detected_ticker:
            chart_fig = make_price_chart(
                detected_ticker,
                fetched_stock.get("name", detected_ticker) if fetched_stock else detected_ticker
            )

        # Load embedding model
        if st.session_state.embedding_model is None:
            st.session_state.embedding_model = load_embedding_model()

        # Build RAG context
        rag_context = build_rag_context(
            query=q,
            news_articles=news_articles,
            stock_context=stock_ctx,
            pdf_index=None, pdf_chunks=[],
            model=st.session_state.embedding_model,
        )

        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": q})

        # Get LLM response
        response = get_llm_response(
            query=q,
            context=rag_context,
            chat_history=st.session_state.chat_history[:-1],
            groq_api_key=GROQ_API_KEY,
        )

        # Add bot message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "stock": fetched_stock,
            "chart": chart_fig,
        })

        st.rerun()

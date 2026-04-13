"""
🌸 FoodTrackr — Pink theme
Usage in every page:
    from theme import PINK_CSS, sidebar, pill
"""

PINK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }



/* backgrounds */
.main, .stApp, [data-testid="stAppViewContainer"] { background-color: #1a0812 !important; }
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(160deg, #1a0812 0%, #22101a 60%, #1a0812 100%) !important;
}
.stSidebar, [data-testid="stSidebar"] {
    background: #130610 !important;
    border-right: 1px solid rgba(255,45,120,0.14) !important;
}
.block-container { padding: 2rem 2.5rem; }

/* typography */
h1,h2,h3 { color: #fff !important; font-family: 'Syne', sans-serif !important; }
p, .stMarkdown p { color: rgba(255,160,210,0.6) !important; }
label { color: rgba(255,160,210,0.65) !important; font-size: 13px !important; }
hr { border-color: rgba(255,45,120,0.12) !important; }

/* hero */
.hero-title { font-family: 'Syne', sans-serif; font-size: 2.8rem; font-weight: 800; color: #fff; line-height: 1.1; margin-bottom: 0.5rem; }
.hero-sub   { font-size: 15px; color: rgba(255,160,210,0.45); margin-bottom: 2rem; max-width: 520px; line-height: 1.7; }

/* page headers */
.page-tag {
    display: inline-block;
    background: rgba(255,45,120,0.12); color: #ff2d78;
    border: 1px solid rgba(255,45,120,0.28);
    padding: 4px 14px; border-radius: 99px;
    font-size: 12px; font-weight: 500; letter-spacing: 0.08em;
    text-transform: uppercase; margin-bottom: 0.75rem;
}
.page-title { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 0.4rem; }
.page-sub   { font-size: 13px; color: rgba(255,160,210,0.4); margin-bottom: 2rem; }

/* stat / kpi cards */
.stat-card, .kpi-card {
    background: #2b1020; border: 1px solid rgba(255,45,120,0.18);
    border-radius: 14px; padding: 1.4rem 1.6rem;
}
.stat-label, .kpi-label {
    font-size: 11px; color: rgba(255,160,210,0.38);
    text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500; margin-bottom: 6px;
}
.stat-value, .kpi-value {
    font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #ff2d78;
}
.stat-sub, .kpi-sub { font-size: 11px; color: rgba(255,160,210,0.32); margin-top: 4px; }

/* nav cards */
.nav-card {
    background: #2b1020; border: 1px solid rgba(255,45,120,0.1);
    border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 10px;
}
.nav-icon  { font-size: 1.6rem; margin-bottom: 8px; }
.nav-title { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 4px; }
.nav-desc  { font-size: 12px; color: rgba(255,160,210,0.36); line-height: 1.6; }


/* form cards */
.form-card {
    background: #2b1020; border: 1px solid rgba(255,45,120,0.18);
    border-radius: 16px; padding: 1.8rem 2rem; margin-bottom: 1.5rem;
}
.form-section {
    font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600;
    color: rgba(255,160,210,0.38); text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 1rem; padding-bottom: 8px; border-bottom: 1px solid rgba(255,45,120,0.08);
}

/* summary / order preview */
.summary-card {
    background: rgba(255,45,120,0.06); border: 1px solid rgba(255,45,120,0.2);
    border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem;
}
.summary-title { font-size: 11px; font-weight: 600; color: #ff2d78; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }
.summary-row   { display: flex; justify-content: space-between; font-size: 13px; color: rgba(255,160,210,0.5); padding: 3px 0; }
.summary-total { display: flex; justify-content: space-between; font-size: 15px; font-weight: 600; color: #fff; padding-top: 8px; margin-top: 6px; border-top: 1px solid rgba(255,45,120,0.08); }

/* winner card */
.winner-card {
    background: linear-gradient(135deg, rgba(255,45,120,0.12), rgba(255,45,120,0.04));
    border: 1px solid rgba(255,45,120,0.32); border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;
}
.winner-label    { font-size: 11px; font-weight: 600; color: #ff2d78; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.winner-platform { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: #fff; margin-bottom: 4px; }
.winner-price    { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 700; color: #ff2d78; }
.winner-saving   { font-size: 13px; color: rgba(255,160,210,0.4); margin-top: 4px; }

/* item cards */
.item-card {
    background: #2b1020; border: 1px solid rgba(255,45,120,0.08);
    border-radius: 12px; padding: 14px 16px; margin-bottom: 8px;
}
.item-name     { font-size: 13px; font-weight: 500; color: #fff; margin-bottom: 4px; }
.item-meta     { font-size: 11px; color: rgba(255,160,210,0.35); }
.item-cheapest { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 700; color: #ff2d78; }

/* platform pills */
.platform-pill  { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: 11px; font-weight: 500; }
.pill-swiggy    { background: rgba(252,88,0,0.15);    color: #fc5800; }
.pill-zomato    { background: rgba(235,67,67,0.15);   color: #eb4343; }
.pill-dominos   { background: rgba(0,109,183,0.15);   color: #5eb0ff; }
.pill-mcdonalds { background: rgba(255,188,0,0.15);   color: #ffbc00; }
.pill-eatclub   { background: rgba(255,111,174,0.15); color: #ff6fae; }
.pill-eatsure   { background: rgba(200,100,219,0.15); color: #d080f0; }
.pill-other     { background: rgba(255,255,255,0.06); color: rgba(255,160,210,0.5); }

/* comparison badges */
.cr-badge    { font-size: 10px; padding: 2px 8px; border-radius: 99px; font-weight: 500; }
.badge-best  { background: rgba(255,45,120,0.15);  color: #ff2d78; }
.badge-save  { background: rgba(255,111,174,0.12); color: #ff6fae; }
.badge-worst { background: rgba(235,67,67,0.1);    color: #eb4343; }

/* chart + insight cards */
.chart-card {
    background: #2b1020; border: 1px solid rgba(255,45,120,0.08);
    border-radius: 16px; padding: 1.5rem; margin-bottom: 1.2rem;
}
.chart-title { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 4px; }
.chart-sub   { font-size: 12px; color: rgba(255,160,210,0.35); margin-bottom: 1rem; }

.insight-card  { background: rgba(255,45,120,0.06); border: 1px solid rgba(255,45,120,0.18); border-radius: 12px; padding: 14px 16px; margin-bottom: 8px; }
.insight-title { font-size: 12px; font-weight: 600; color: #ff2d78; margin-bottom: 4px; }
.insight-text  { font-size: 13px; color: rgba(255,160,210,0.55); line-height: 1.6; }

.top-item       { background: #2b1020; border: 1px solid rgba(255,45,120,0.08); border-radius: 10px; padding: 12px 14px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
.top-item-name  { font-size: 13px; font-weight: 500; color: #fff; }
.top-item-count { font-size: 11px; color: rgba(255,160,210,0.32); margin-top: 2px; }
.top-item-price { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #ff2d78; }

/* budget */
.budget-hero { border-radius: 20px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; border: 1px solid rgba(255,45,120,0.1); position: relative; overflow: hidden; }
.budget-hero.safe   { background: linear-gradient(135deg, #0a1f0a, #0f2d0f); border-color: rgba(80,200,120,0.22); }
.budget-hero.warn   { background: linear-gradient(135deg, #1f1700, #2a2000); border-color: rgba(255,188,0,0.22); }
.budget-hero.danger { background: linear-gradient(135deg, #1f0812, #2a0f1a); border-color: rgba(255,45,120,0.32); }
.budget-hero.none   { background: linear-gradient(135deg, #2b1020, #381528); border-color: rgba(255,45,120,0.14); }
.bh-status  { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.bh-amount  { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #fff; line-height: 1; margin-bottom: 6px; }
.bh-sub     { font-size: 13px; color: rgba(255,160,210,0.4); margin-bottom: 1.2rem; }
.bh-bar-wrap { background: rgba(255,255,255,0.08); border-radius: 99px; height: 8px; margin-bottom: 8px; overflow: hidden; }
.bh-bar      { height: 100%; border-radius: 99px; }
.bh-bar.safe   { background: #50c878; }
.bh-bar.warn   { background: #ffbc00; }
.bh-bar.danger { background: #eb4343; }
.bh-bar-labels { display: flex; justify-content: space-between; font-size: 11px; color: rgba(255,160,210,0.3); }

.stat-card .val-green  { color: #50c878; }
.stat-card .val-orange { color: #ff6fae; }
.stat-card .val-red    { color: #eb4343; }
.stat-card .val-yellow { color: #ffbc00; }

.form-card .tip-row   { background: rgba(255,45,120,0.05); border: 1px solid rgba(255,45,120,0.14); border-radius: 12px; padding: 12px 16px; margin-bottom: 8px; }
.form-card .tip-title { font-size: 11px; font-weight: 600; color: #ff2d78; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.form-card .tip-text  { font-size: 12px; color: rgba(255,160,210,0.45); line-height: 1.6; }
.history-row  { background: #2b1020; border: 1px solid rgba(255,45,120,0.08); border-radius: 10px; padding: 12px 16px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
.hr-month  { font-size: 13px; font-weight: 500; color: #fff; }
.hr-meta   { font-size: 11px; color: rgba(255,160,210,0.32); margin-top: 2px; }
.hr-budget { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #ff2d78; }

/* streamlit widget overrides */
.stButton > button {
    background: linear-gradient(135deg, #ff2d78, #c0184a) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-family: 'Syne', sans-serif !important;
    width: 100% !important; padding: 0.65rem !important;
    box-shadow: 0 4px 14px rgba(255,45,120,0.28) !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

.del-btn > button {
    background: rgba(235,67,67,0.1) !important; color: #eb4343 !important;
    border: 1px solid rgba(235,67,67,0.2) !important;
    font-size: 12px !important; padding: 0.3rem 0.8rem !important; width: auto !important;
    box-shadow: none !important;
}

[data-testid="stSelectbox"] > div,
[data-testid="stTextInput"] > div > div,
[data-testid="stNumberInput"] > div > div {
    background: #130610 !important; border-color: rgba(255,45,120,0.2) !important;
    color: #fff !important; border-radius: 8px !important;
}
.stSuccess { background: rgba(255,45,120,0.1)  !important; color: #ff6fae !important; border: 1px solid rgba(255,45,120,0.22) !important; border-radius: 8px !important; }
.stError   { background: rgba(235,67,67,0.1)   !important; color: #f09595 !important; border: 1px solid rgba(235,67,67,0.22)  !important; border-radius: 8px !important; }
.stWarning { background: rgba(255,188,0,0.08)  !important; color: #ffbc00 !important; border: 1px solid rgba(255,188,0,0.2)   !important; border-radius: 8px !important; }
.stInfo    { background: rgba(255,45,120,0.07) !important; color: #ff6fae !important; border: 1px solid rgba(255,45,120,0.18) !important; border-radius: 8px !important; }
hr { border-color: rgba(255,45,120,0.1) !important; }
</style>
"""

SIDEBAR_HTML = """
<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;
     background:linear-gradient(90deg,#ff2d78,#ff6fae);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
     margin-bottom:0.15rem">FoodTrackr</div>
<div style="font-size:11px;color:rgba(255,120,180,0.38);margin-bottom:1.5rem">
     Student Edition — Pune</div>
"""

def apply_theme():
    import streamlit as st
    st.markdown(PINK_CSS, unsafe_allow_html=True)

def sidebar():
    import streamlit as st
    with st.sidebar:
        st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
        st.markdown("---")
        st.page_link("app.py",                      label="🏠  Home")
        st.page_link("pages/log_order.py",         label="✏️  Log Order")
        st.page_link("pages/price_comparision.py",  label="💰  Price Compare")
        st.page_link("pages/spend_tracker.py",     label="📊  Spend Tracker")
        st.page_link("pages/budget.py",            label="🎯  Budget")

def pill(platform: str) -> str:
    p = platform.lower()
    if   "swiggy"   in p: css = "pill-swiggy"
    elif "zomato"   in p: css = "pill-zomato"
    elif "domino"   in p: css = "pill-dominos"
    elif "mcdonald" in p or "mcd" in p: css = "pill-mcdonalds"
    elif "eatclub"  in p: css = "pill-eatclub"
    elif "eatsure"  in p: css = "pill-eatsure"
    else:                  css = "pill-other"
    return f'<span class="platform-pill {css}">{platform}</span>'

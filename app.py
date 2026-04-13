import streamlit as st
import sys, os
sys.path.append(os.path.dirname(__file__))
from db import get_connection
from theme import apply_theme, sidebar
from datetime import date
import calendar

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.set_page_config(page_title="FoodTrackr", page_icon="🌸", layout="wide")
apply_theme()
sidebar()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem">
    <div class="hero-title">Your food,<br>
    <span style="background:linear-gradient(90deg,#ff2d78,#ff6fae);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
    tracked &amp; compared.</span></div>
    <div class="hero-sub">Stop juggling Swiggy, Zomato, EatClub tabs.
    Log your orders, compare prices, and keep your food budget in check — all in one place.</div>
</div>
""", unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────────────────────
try:
    conn      = get_connection()
    cursor    = conn.cursor()
    today     = date.today()
    month_str = today.strftime("%Y-%m")
    first_day = today.replace(day=1)
    last_day  = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(total),0) FROM orders WHERE order_date BETWEEN %s AND %s",
        (first_day, last_day)
    )
    month_spend = float(cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(DISTINCT item_name) FROM price_comparison")
    tracked_items = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(monthly_limit,0) FROM budget WHERE month=%s", (month_str,))
    row    = cursor.fetchone()
    budget = float(row[0]) if row else 0
    remaining = budget - month_spend if budget > 0 else None
    conn.close()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Total orders</div><div class="stat-value">{total_orders}</div><div class="stat-sub">all time</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Spent this month</div><div class="stat-value">₹{month_spend:,.0f}</div><div class="stat-sub">{today.strftime("%B %Y")}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Items tracked</div><div class="stat-value">{tracked_items}</div><div class="stat-sub">in price compare</div></div>', unsafe_allow_html=True)
    with c4:
        if remaining is not None:
            color = "#eb4343" if remaining < 0 else "#50c878"
            label = "Over budget" if remaining < 0 else "Budget left"
            st.markdown(f'<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-value" style="color:{color}">₹{abs(remaining):,.0f}</div><div class="stat-sub">this month</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="stat-card"><div class="stat-label">Budget left</div><div class="stat-value" style="color:rgba(255,160,210,0.2)">—</div><div class="stat-sub">no budget set</div></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Could not connect to database: {e}")

#Navigation cards
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:rgba(255,120,180,0.35);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1rem">Go to</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="nav-card"><div class="nav-icon">✏️</div><div class="nav-title">Log Order</div><div class="nav-desc">Add a new order with price breakdown</div></div>', unsafe_allow_html=True)
    st.page_link("pages/log_order.py", label="Open →")
with col2:
    st.markdown('<div class="nav-card"><div class="nav-icon">💰</div><div class="nav-title">Price Compare</div><div class="nav-desc">See the cheapest platform for any dish</div></div>', unsafe_allow_html=True)
    st.page_link("pages/price_comparision.py", label="Open →")
with col3:
    st.markdown('<div class="nav-card"><div class="nav-icon">📊</div><div class="nav-title">Spend Tracker</div><div class="nav-desc">Charts and insights on your spending</div></div>', unsafe_allow_html=True)
    st.page_link("pages/spend_tracker.py", label="Open →")
with col4:
    st.markdown('<div class="nav-card"><div class="nav-icon">🎯</div><div class="nav-title">Budget</div><div class="nav-desc">Set and track your monthly food budget</div></div>', unsafe_allow_html=True)
    st.page_link("pages/budget.py", label="Open →")

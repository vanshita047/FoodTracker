import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_connection
from theme import apply_theme, sidebar
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objects as go
import calendar

st.set_page_config(page_title="Budget", page_icon="🎯", layout="wide")
apply_theme()
sidebar()

#Plotly pink theme
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="rgba(255,160,210,0.6)", size=12),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor="rgba(255,45,120,0.06)", tickfont=dict(color="rgba(255,160,210,0.4)")),
    yaxis=dict(gridcolor="rgba(255,45,120,0.06)", tickfont=dict(color="rgba(255,160,210,0.4)")),
)

#DB helpers
def get_budget(month_str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT monthly_limit FROM budget WHERE month = %s", (month_str,))
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0

def set_budget(month_str, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budget (month, monthly_limit) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE monthly_limit = %s
    """, (month_str, amount, amount))
    conn.commit()
    conn.close()

def get_monthly_spend(month_str):
    conn = get_connection()
    cursor = conn.cursor()
    year, month = map(int, month_str.split('-'))
    first_day = date(year, month, 1)
    last_day  = date(year, month, calendar.monthrange(year, month)[1])
    cursor.execute("""
        SELECT COALESCE(SUM(total), 0) FROM orders
        WHERE order_date BETWEEN %s AND %s
    """, (first_day, last_day))
    result = cursor.fetchone()[0]
    conn.close()
    return float(result)

def get_daily_spend_this_month():
    conn = get_connection()
    today = date.today()
    first_day = today.replace(day=1)
    df = pd.read_sql("""
        SELECT order_date, SUM(total) as daily_total
        FROM orders WHERE order_date >= %s
        GROUP BY order_date ORDER BY order_date ASC
    """, conn, params=(first_day,))
    conn.close()
    if not df.empty:
        df['order_date']  = pd.to_datetime(df['order_date'])
        df['daily_total'] = df['daily_total'].astype(float)
    return df

def get_budget_history():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT month, monthly_limit FROM budget ORDER BY month DESC LIMIT 6")
    rows = cursor.fetchall()
    conn.close()
    return rows

#Header
st.markdown("""
<div>
    <div class="page-tag">Budget</div>
    <div class="page-title">Set your monthly limit</div>
    <div class="page-sub">Know exactly how much you can spend each day so you never run out</div>
</div>
""", unsafe_allow_html=True)

today         = date.today()
current_month = today.strftime("%Y-%m")
month_label   = today.strftime("%B %Y")
days_in_month = calendar.monthrange(today.year, today.month)[1]
days_passed   = today.day
days_left     = days_in_month - today.day

current_budget = get_budget(current_month)
current_spend  = get_monthly_spend(current_month)
remaining      = current_budget - current_spend if current_budget > 0 else 0
budget_pct     = (current_spend / current_budget * 100) if current_budget > 0 else 0
safe_per_day   = remaining / days_left if days_left > 0 and remaining > 0 else 0
ideal_per_day  = current_budget / days_in_month if current_budget > 0 else 0
expected_spend = (current_spend / days_passed) * days_in_month if days_passed > 0 else 0

left_col, right_col = st.columns([1.5, 1])

with left_col:
    # Budget hero card
    if current_budget == 0:
        hero_class, status_text, status_color = "none", "No budget set", "#ff6fae"
    elif budget_pct >= 90:
        hero_class, status_text, status_color = "danger", "Critical — almost out of budget", "#eb4343"
    elif budget_pct >= 70:
        hero_class, status_text, status_color = "warn", "Warning — spending fast", "#ffbc00"
    else:
        hero_class, status_text, status_color = "safe", "On track — keep it up 🌸", "#50c878"

    bar_class = "danger" if budget_pct >= 90 else ("warn" if budget_pct >= 70 else "safe")
    bar_width = min(budget_pct, 100)

    if current_budget > 0:
        st.markdown(f"""
        <div class="budget-hero {hero_class}">
            <div class="bh-status" style="color:{status_color}">{status_text}</div>
            <div class="bh-amount">₹{remaining:,.0f}</div>
            <div class="bh-sub">remaining of ₹{current_budget:,.0f} budget for {month_label}</div>
            <div class="bh-bar-wrap"><div class="bh-bar {bar_class}" style="width:{bar_width}%"></div></div>
            <div class="bh-bar-labels">
                <span>₹0</span>
                <span>₹{current_spend:,.0f} spent ({budget_pct:.0f}%)</span>
                <span>₹{current_budget:,.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="budget-hero none">
            <div class="bh-status" style="color:#ff6fae">No budget set for {month_label}</div>
            <div class="bh-amount" style="color:rgba(255,160,210,0.25)">₹—</div>
            <div class="bh-sub">Set a budget on the right to start tracking</div>
        </div>
        """, unsafe_allow_html=True)

    # Stats row
    s1, s2, s3 = st.columns(3)
    with s1:
        color = "val-green" if safe_per_day > 0 else "val-orange"
        st.markdown(f'<div class="stat-card"><div class="stat-label">Safe to spend today</div><div class="stat-value {color}">₹{safe_per_day:,.0f}</div><div class="stat-sub">per day for {days_left} days left</div></div>', unsafe_allow_html=True)
    with s2:
        color = "val-green" if expected_spend <= current_budget else "val-red"
        st.markdown(f'<div class="stat-card"><div class="stat-label">Projected month total</div><div class="stat-value {color}">₹{expected_spend:,.0f}</div><div class="stat-sub">at current pace</div></div>', unsafe_allow_html=True)
    with s3:
        diff  = abs(expected_spend - current_budget) if current_budget > 0 else 0
        over  = expected_spend > current_budget and current_budget > 0
        color = "val-red" if over else "val-green"
        label = "Over budget by" if over else "Under budget by"
        st.markdown(f'<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-value {color}">₹{diff:,.0f}</div><div class="stat-sub">projected</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Daily spend chart
    daily_df = get_daily_spend_this_month()
    if not daily_df.empty and current_budget > 0:
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:14px;font-weight:700;color:#fff;margin-bottom:0.5rem">Daily spend this month</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_hline(y=ideal_per_day, line_dash="dash",
                      line_color="rgba(255,45,120,0.4)", line_width=1,
                      annotation_text=f"Ideal: ₹{ideal_per_day:,.0f}/day",
                      annotation_font_color="rgba(255,111,174,0.6)", annotation_font_size=10)
        bar_colors = ['#eb4343' if v > ideal_per_day*1.5 else '#ff2d78' if v > ideal_per_day else '#50c878'
                      for v in daily_df['daily_total']]
        fig.add_trace(go.Bar(
            x=daily_df['order_date'], y=daily_df['daily_total'],
            marker_color=bar_colors,
            hovertemplate='%{x|%d %b}<br>₹%{y:,.0f}<extra></extra>'
        ))
        fig.update_layout(**PLOTLY_THEME, height=200, bargap=0.3)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with right_col:
    # Set budget form
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-section">Set budget for this month</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:13px;font-weight:500;color:rgba(255,160,210,0.6);margin-bottom:12px">{month_label}</div>', unsafe_allow_html=True)

    new_budget = st.number_input(
        "Monthly food budget (₹)",
        min_value=0.0,
        value=float(current_budget) if current_budget > 0 else 2000.0,
        step=100.0
    )
    implied_daily = new_budget / days_in_month if new_budget > 0 else 0
    st.markdown(f'<div style="font-size:12px;color:rgba(255,160,210,0.35);margin-bottom:12px">= ₹{implied_daily:,.0f} per day for {days_in_month} days</div>', unsafe_allow_html=True)

    if st.button("Save Budget"):
        if new_budget <= 0:
            st.error("Please enter a valid budget amount.")
        else:
            set_budget(current_month, new_budget)
            st.success(f"Budget set to ₹{new_budget:,.0f} for {month_label}!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Tips
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:#fff;margin-bottom:0.75rem">Money saving tips 🌸</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,45,120,0.05);border:1px solid rgba(255,45,120,0.14);border-radius:12px;padding:12px 16px;margin-bottom:8px">
        <div style="font-size:11px;font-weight:600;color:#ff2d78;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Order above the threshold</div>
        <div style="font-size:12px;color:rgba(255,160,210,0.45);line-height:1.6">Most apps waive delivery fees above ₹149–199. Add one extra item instead of paying ₹30–50 delivery.</div>
    </div>
    <div style="background:rgba(255,45,120,0.05);border:1px solid rgba(255,45,120,0.14);border-radius:12px;padding:12px 16px;margin-bottom:8px">
        <div style="font-size:11px;font-weight:600;color:#ff2d78;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Use lunch offers</div>
        <div style="font-size:12px;color:rgba(255,160,210,0.45);line-height:1.6">Swiggy and Zomato both offer 40–60% off between 11am–2pm. Same food, half the price.</div>
    </div>
    <div style="background:rgba(255,45,120,0.05);border:1px solid rgba(255,45,120,0.14);border-radius:12px;padding:12px 16px;margin-bottom:8px">
        <div style="font-size:11px;font-weight:600;color:#ff2d78;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">EatClub for dinner</div>
        <div style="font-size:12px;color:rgba(255,160,210,0.45);line-height:1.6">EatClub specialises in evening meals at 50% off. Great for biryani and thali under ₹100.</div>
    </div>
    <div style="background:rgba(255,45,120,0.05);border:1px solid rgba(255,45,120,0.14);border-radius:12px;padding:12px 16px;margin-bottom:8px">
        <div style="font-size:11px;font-weight:600;color:#ff2d78;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Check all three apps</div>
        <div style="font-size:12px;color:rgba(255,160,210,0.45);line-height:1.6">The same restaurant lists on Swiggy and Zomato at different prices. Always check both before ordering.</div>
    </div>
    """, unsafe_allow_html=True)

    # Budget history
    history = get_budget_history()
    if len(history) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:#fff;margin-bottom:0.75rem">Budget history</div>', unsafe_allow_html=True)
        for h in history:
            year, month = map(int, h['month'].split('-'))
            month_name   = date(year, month, 1).strftime("%B %Y")
            actual_spend = get_monthly_spend(h['month'])
            pct   = (actual_spend / float(h['monthly_limit']) * 100)
            color = "#eb4343" if pct > 100 else ("#ffbc00" if pct > 80 else "#50c878")
            st.markdown(f"""
            <div class="history-row">
                <div>
                    <div class="hr-month">{month_name}</div>
                    <div class="hr-meta">Spent ₹{actual_spend:,.0f} of ₹{float(h['monthly_limit']):,.0f} — <span style="color:{color}">{pct:.0f}%</span></div>
                </div>
                <div class="hr-budget">₹{float(h['monthly_limit']):,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_connection
from theme import apply_theme, sidebar
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Spend Tracker", page_icon="📊", layout="wide")
apply_theme()

#Sidebar (with filter) 
with st.sidebar:
    from theme import SIDEBAR_HTML, PINK_CSS
    st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                      label="🏠  Home")
    st.page_link("pages/log_order.py",         label="✏️  Log Order")
    st.page_link("pages/price_comparision.py",  label="💰  Price Compare")
    st.page_link("pages/spend_tracker.py",     label="📊  Spend Tracker")
    st.page_link("pages/budget.py",            label="🎯  Budget")
    st.markdown("---")
    st.markdown("**Filter**")
    time_range = st.selectbox("Time range", ["Last 7 days", "Last 30 days", "Last 90 days", "All time"])

#Plotly pink theme 
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="rgba(255,160,210,0.6)", size=12),
    margin=dict(l=10, r=10, t=10, b=10),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(255,160,210,0.5)", size=11)),
    xaxis=dict(gridcolor="rgba(255,45,120,0.06)", zerolinecolor="rgba(255,45,120,0.08)", tickfont=dict(color="rgba(255,160,210,0.4)")),
    yaxis=dict(gridcolor="rgba(255,45,120,0.06)", zerolinecolor="rgba(255,45,120,0.08)", tickfont=dict(color="rgba(255,160,210,0.4)")),
)

PLATFORM_COLORS = {
    "Swiggy": "#fc5800", "Zomato": "#eb4343", "Dominos": "#5eb0ff",
    "McDonalds": "#ffbc00", "EatClub": "#ff6fae", "EatSure": "#d080f0", "Other": "#888888"
}

def get_orders_df(days=30):
    conn  = get_connection()
    since = date.today() - timedelta(days=days)
    df = pd.read_sql("""
        SELECT order_date, platform, restaurant, item_name,
               quantity, price, delivery_fee, discount, total
        FROM orders WHERE order_date >= %s ORDER BY order_date ASC
    """, conn, params=(since,))
    conn.close()
    if not df.empty:
        df['order_date']   = pd.to_datetime(df['order_date'])
        df['total']        = df['total'].astype(float)
        df['delivery_fee'] = df['delivery_fee'].astype(float)
        df['discount']     = df['discount'].astype(float)
    return df

#Header 
st.markdown("""
<div>
    <div class="page-tag">Spend Tracker</div>
    <div class="page-title">Where is your money going?</div>
    <div class="page-sub">Charts and insights from your order history</div>
</div>
""", unsafe_allow_html=True)

days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90, "All time": 3650}
days = days_map[time_range]
df   = get_orders_df(days)

if df.empty:
    st.info("No orders found for this period. Log some orders first!")
    st.stop()

#KPIs
total_spend    = df['total'].sum()
order_count    = len(df)
avg_order      = df['total'].mean()
total_delivery = df['delivery_fee'].sum()
total_discount = df['discount'].sum()
avg_per_day    = total_spend / max(days, 1)
most_used      = df['platform'].value_counts().index[0]

k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total spent</div><div class="kpi-value">₹{total_spend:,.0f}</div><div class="kpi-sub">{time_range.lower()}</div></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Orders placed</div><div class="kpi-value">{order_count}</div><div class="kpi-sub">avg ₹{avg_order:,.0f} each</div></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Daily average</div><div class="kpi-value">₹{avg_per_day:,.0f}</div><div class="kpi-sub">per day</div></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Delivery fees paid</div><div class="kpi-value">₹{total_delivery:,.0f}</div><div class="kpi-sub">avoidable cost</div></div>', unsafe_allow_html=True)
with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Saved via discounts</div><div class="kpi-value">₹{total_discount:,.0f}</div><div class="kpi-sub">via offers & coupons</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

#Charts row 1
chart1, chart2 = st.columns([1.6, 1])

with chart1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Daily spending trend</div><div class="chart-sub">How much you spent each day</div>', unsafe_allow_html=True)
    daily = df.groupby('order_date')['total'].sum().reset_index()
    daily.columns = ['date', 'total']
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily['date'], y=daily['total'],
        fill='tozeroy', fillcolor='rgba(255,45,120,0.08)',
        line=dict(color='#ff2d78', width=2),
        mode='lines+markers', marker=dict(size=5, color='#ff2d78'),
        hovertemplate='%{x|%d %b}<br>₹%{y:,.0f}<extra></extra>'
    ))
    fig.update_layout(**PLOTLY_THEME, height=220)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with chart2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Spend by platform</div><div class="chart-sub">Which app gets most of your money</div>', unsafe_allow_html=True)
    platform_spend = df.groupby('platform')['total'].sum().reset_index()
    platform_spend.columns = ['platform', 'total']
    platform_spend = platform_spend.sort_values('total', ascending=False)
    colors = [PLATFORM_COLORS.get(p, '#888888') for p in platform_spend['platform']]
    fig2 = go.Figure(go.Pie(
        labels=platform_spend['platform'], values=platform_spend['total'],
        hole=0.6, marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=11, color='rgba(255,160,210,0.7)'),
        hovertemplate='%{label}<br>₹%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    fig.update_layout(**PLOTLY_THEME, height=220)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

#Charts row 2 
chart3, chart4 = st.columns(2)

with chart3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Weekly spending</div><div class="chart-sub">Spending grouped by week</div>', unsafe_allow_html=True)
    df['week'] = df['order_date'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly = df.groupby('week')['total'].sum().reset_index()
    weekly.columns = ['week', 'total']
    fig3 = go.Figure(go.Bar(
        x=weekly['week'], y=weekly['total'],
        marker_color='#ff2d78', marker_opacity=0.8,
        hovertemplate='Week of %{x|%d %b}<br>₹%{y:,.0f}<extra></extra>'
    ))
    fig3.update_layout(**PLOTLY_THEME, height=220, bargap=0.3)
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with chart4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Orders by day of week</div><div class="chart-sub">Which days you order most</div>', unsafe_allow_html=True)
    df['day_of_week'] = df['order_date'].dt.day_name()
    day_order  = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_counts = df.groupby('day_of_week')['total'].sum().reindex(day_order, fill_value=0).reset_index()
    day_counts.columns = ['day', 'total']
    fig4 = go.Figure(go.Bar(
        x=day_counts['day'], y=day_counts['total'],
        marker_color=['#ff2d78' if d in ['Friday','Saturday','Sunday'] else 'rgba(255,45,120,0.3)' for d in day_counts['day']],
        hovertemplate='%{x}<br>₹%{y:,.0f}<extra></extra>'
    ))
    fig4.update_layout(**PLOTLY_THEME, height=220, bargap=0.3)
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

#Top items + Insights 
st.markdown("---")
items_col, insights_col = st.columns([1, 1])

with items_col:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:14px;font-weight:700;color:#fff;margin-bottom:1rem">Most ordered items</div>', unsafe_allow_html=True)
    top_items = df.groupby('item_name').agg(
        total_spent=('total', 'sum'),
        order_count=('item_name', 'count')
    ).sort_values('total_spent', ascending=False).head(7).reset_index()

    for _, row in top_items.iterrows():
        st.markdown(f"""
        <div class="top-item">
            <div>
                <div class="top-item-name">{row['item_name']}</div>
                <div class="top-item-count">Ordered {int(row['order_count'])} time{'s' if row['order_count'] > 1 else ''}</div>
            </div>
            <div class="top-item-price">₹{float(row['total_spent']):,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

with insights_col:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:14px;font-weight:700;color:#fff;margin-bottom:1rem">Smart insights</div>', unsafe_allow_html=True)

    most_expensive_day    = df.groupby('order_date')['total'].sum().idxmax()
    most_expensive_amount = df.groupby('order_date')['total'].sum().max()
    top_platform          = df.groupby('platform')['total'].sum().idxmax()
    top_platform_pct      = (df.groupby('platform')['total'].sum().max() / total_spend * 100)
    delivery_pct          = (total_delivery / total_spend * 100) if total_spend > 0 else 0
    monthly_projection    = avg_per_day * 30

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">Biggest spending day</div>
        <div class="insight-text">You spent the most on <strong style="color:#fff">{most_expensive_day.strftime('%d %b %Y')}</strong> — a total of <strong style="color:#ff2d78">₹{most_expensive_amount:,.0f}</strong>. What happened that day?</div>
    </div>
    <div class="insight-card">
        <div class="insight-title">Platform loyalty</div>
        <div class="insight-text"><strong style="color:#fff">{top_platform}</strong> takes <strong style="color:#ff2d78">{top_platform_pct:.0f}%</strong> of your food budget. Try switching platforms — same food, better deals.</div>
    </div>
    <div class="insight-card">
        <div class="insight-title">Delivery fee drain</div>
        <div class="insight-text">You've paid <strong style="color:#ff2d78">₹{total_delivery:,.0f}</strong> in delivery fees — that's <strong style="color:#fff">{delivery_pct:.0f}%</strong> of total spend. Order above the free delivery threshold to save more.</div>
    </div>
    <div class="insight-card">
        <div class="insight-title">Monthly projection</div>
        <div class="insight-text">At your current pace you'll spend <strong style="color:#ff2d78">₹{monthly_projection:,.0f}</strong> this month on food. Is that within your budget?</div>
    </div>
    """, unsafe_allow_html=True)

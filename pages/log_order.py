import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_connection
from theme import apply_theme, sidebar, pill
from datetime import date

st.set_page_config(page_title="Log Order", page_icon="✏️", layout="wide")
apply_theme()
sidebar()

#DB helper
def log_order(order_date, platform, restaurant, item_name, quantity, price, delivery_fee, discount):
    total = (price * quantity) + delivery_fee - discount
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_date, platform, restaurant, item_name, quantity, price, delivery_fee, discount, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (order_date, platform, restaurant, item_name, quantity, price, delivery_fee, discount, total))
    conn.commit()
    conn.close()

def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, order_date, platform, restaurant, item_name, quantity,
               price, delivery_fee, discount, total
        FROM orders ORDER BY id DESC LIMIT 30
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    conn.commit()
    conn.close()

#Header 
st.markdown("""
<div class="page-header">
    <div class="page-tag">Log Order</div>
    <div class="page-title">Add a new order</div>
    <div class="page-sub">Log what you ordered, where from, and how much it cost</div>
</div>
""", unsafe_allow_html=True)

#Layout
form_col, preview_col = st.columns([1.4, 1])

with form_col:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-section">Order details</div>', unsafe_allow_html=True)

    row1a, row1b = st.columns(2)
    with row1a:
        order_date = st.date_input("Order date", value=date.today())
    with row1b:
        platform = st.selectbox("Platform", [
            "Swiggy", "Zomato", "Dominos", "McDonalds", "EatClub", "EatSure", "Other"
        ])

    restaurant = st.text_input("Restaurant name", placeholder="e.g. Behrouz Biryani, Burger King")
    item_name  = st.text_input("What did you order?", placeholder="e.g. Chicken Biryani, Margherita Pizza")

    row2a, row2b = st.columns(2)
    with row2a:
        quantity = st.number_input("Quantity", min_value=1, max_value=20, value=1)
    with row2b:
        price = st.number_input("Item price (₹)", min_value=0.0, value=0.0, step=5.0)

    row3a, row3b = st.columns(2)
    with row3a:
        delivery_fee = st.number_input("Delivery fee (₹)", min_value=0.0, value=0.0, step=5.0)
    with row3b:
        discount = st.number_input("Discount / offer (₹)", min_value=0.0, value=0.0, step=5.0)

    st.markdown('</div>', unsafe_allow_html=True)

    total_preview = (price * quantity) + delivery_fee - discount

    if st.button("Save Order"):
        if not item_name.strip():
            st.error("Please enter what you ordered.")
        elif price <= 0:
            st.error("Please enter a valid price.")
        else:
            try:
                log_order(order_date, platform, restaurant.strip(), item_name.strip(),
                          quantity, price, delivery_fee, discount)
                st.success(f"Order logged! ₹{total_preview:,.0f} spent on {item_name} from {platform}.")
                st.balloons()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

with preview_col:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:13px;font-weight:600;color:rgba(255,120,180,0.4);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1rem">Order summary</div>', unsafe_allow_html=True)

    total_preview = (price * quantity) + delivery_fee - discount
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-title">Price breakdown</div>
        <div class="summary-row"><span>Item price</span><span>₹{price:,.0f} × {quantity}</span></div>
        <div class="summary-row"><span>Delivery fee</span><span>₹{delivery_fee:,.0f}</span></div>
        <div class="summary-row"><span>Discount</span><span style="color:#50c878">- ₹{discount:,.0f}</span></div>
        <div class="summary-total"><span>Total</span><span>₹{total_preview:,.0f}</span></div>
    </div>
    """, unsafe_allow_html=True)

    if item_name:
        pill_html = pill(platform)
        st.markdown(f"""
        <div style="background:#2b1020;border:1px solid rgba(255,45,120,0.1);border-radius:12px;padding:14px 16px">
            <div style="font-size:13px;font-weight:500;color:#fff;margin-bottom:6px">{item_name}</div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                {pill_html}
                <span style="font-size:11px;color:rgba(255,160,210,0.35)">{restaurant or 'Restaurant'}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:11px;color:rgba(255,160,210,0.35)">{order_date}</span>
                <span style="font-family:Syne,sans-serif;font-size:15px;font-weight:700;color:#ff2d78">₹{total_preview:,.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    days_in_month = 30
    days_left = days_in_month - date.today().day
    if total_preview > 0 and days_left > 0:
        monthly_equiv = total_preview * days_in_month
        st.markdown(f"""
        <div style="background:rgba(255,45,120,0.04);border:1px solid rgba(255,45,120,0.1);border-radius:12px;padding:14px 16px;margin-top:8px">
            <div style="font-size:11px;font-weight:600;color:rgba(255,120,180,0.35);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">If you spend this daily</div>
            <div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:700;color:#ff2d78">₹{monthly_equiv:,.0f}<span style="font-size:13px;font-weight:400;color:rgba(255,160,210,0.35)">/month</span></div>
            <div style="font-size:12px;color:rgba(255,160,210,0.32);margin-top:4px">{days_left} days left this month</div>
        </div>
        """, unsafe_allow_html=True)

#Recent orders
st.markdown("---")
st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:1rem">Recent orders</div>', unsafe_allow_html=True)

orders = get_all_orders()
if orders:
    col_filter1, col_filter2, _ = st.columns([1, 1, 2])
    with col_filter1:
        platforms = ["All"] + sorted(set(o['platform'] for o in orders))
        filter_platform = st.selectbox("Filter by platform", platforms)
    with col_filter2:
        filter_search = st.text_input("Search item", placeholder="e.g. biryani")

    filtered = orders
    if filter_platform != "All":
        filtered = [o for o in filtered if o['platform'] == filter_platform]
    if filter_search:
        filtered = [o for o in filtered if filter_search.lower() in o['item_name'].lower()]

    for order in filtered:
        pill_html = pill(order['platform'])
        col_info, col_price, col_del = st.columns([3, 1, 0.5])
        with col_info:
            st.markdown(f"""
            <div style="padding:8px 0">
                <div style="font-size:13px;font-weight:500;color:#fff;margin-bottom:4px">
                    {order['item_name']} <span style="font-size:11px;color:rgba(255,160,210,0.3)">× {order['quantity']}</span>
                </div>
                <div style="display:flex;align-items:center;gap:8px">
                    {pill_html}
                    <span style="font-size:11px;color:rgba(255,160,210,0.3)">{order['restaurant'] or ''} · {order['order_date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_price:
            st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:15px;font-weight:700;color:#ff2d78;padding-top:12px">₹{float(order["total"]):,.0f}</div>', unsafe_allow_html=True)
        with col_del:
            st.markdown('<div class="del-btn">', unsafe_allow_html=True)
            if st.button("✕", key=f"del_{order['id']}"):
                delete_order(order['id'])
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<hr style="margin:4px 0;border-color:rgba(255,45,120,0.06)">', unsafe_allow_html=True)
else:
    st.info("No orders yet. Log your first order above!")

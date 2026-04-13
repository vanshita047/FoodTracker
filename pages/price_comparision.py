import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_connection
from theme import apply_theme, sidebar, pill
from price_data import seed_prices
from datetime import date

st.set_page_config(page_title="Price Compare", page_icon="💰", layout="wide")
apply_theme()
sidebar()

#DB helpers
def add_price_entry(item_name, platform, restaurant, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO price_comparison (item_name, platform, restaurant, price, last_updated)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE price=%s, restaurant=%s, last_updated=%s
    """, (item_name, platform, restaurant, price, date.today(),
          price, restaurant, date.today()))
    conn.commit()
    conn.close()

def get_all_items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT item_name,
               COUNT(*) as platform_count,
               MIN(price) as min_price,
               MAX(price) as max_price,
               (SELECT platform FROM price_comparison p2
                WHERE p2.item_name = p1.item_name
                ORDER BY price ASC LIMIT 1) as cheapest_platform
        FROM price_comparison p1
        GROUP BY item_name ORDER BY item_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_item_prices(item_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT platform, restaurant, price, last_updated
        FROM price_comparison WHERE item_name=%s ORDER BY price ASC
    """, (item_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_price_entry(item_name, platform):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM price_comparison WHERE item_name=%s AND platform=%s", (item_name, platform))
    conn.commit()
    conn.close()

#Header 
st.markdown("""
<div>
    <div class="page-tag">💰 Price Compare</div>
    <div class="page-title">Find the cheapest platform</div>
    <div class="page-sub">Add prices for the same item across apps — instantly see where to order from</div>
</div>
""", unsafe_allow_html=True)

#Dataset loader banner 
existing = get_all_items()
if not existing:
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(255,45,120,0.1),rgba(255,45,120,0.04));
         border:1px solid rgba(255,45,120,0.28);border-radius:14px;
         padding:1.2rem 1.5rem;margin-bottom:1.5rem">
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#fff;margin-bottom:4px">
            🌸No prices yet — load dataset?</div>
        <div style="font-size:13px;color:rgba(255,160,210,0.55)">
            Pulls real food prices from the Zomato India dataset. Falls back to built-in Pune prices if offline.</div>
    </div>
    """, unsafe_allow_html=True)
    col_live, col_bundled, _ = st.columns([1, 1, 2])
    with col_live:
        if st.button("Load from Kaggle / GitHub"):
            with st.spinner("Fetching live data..."):
                ins, sk, source = seed_prices(use_live=True)
            st.success(f"Loaded {ins} prices · source: {source}")
            st.rerun()
    with col_bundled:
        if st.button("Load built-in Pune prices"):
            with st.spinner("Loading..."):
                ins, sk, source = seed_prices(use_live=False)
            st.success(f"Loaded {ins} prices · source: {source}")
            st.rerun()
else:
    with st.expander("Dataset loaded — click to refresh or re-seed"):
        col_live, col_bundled, _ = st.columns([1, 1, 2])
        with col_live:
            if st.button("Refresh from Kaggle / GitHub"):
                with st.spinner("Fetching..."):
                    ins, sk, source = seed_prices(use_live=True)
                st.success(f"Added {ins} new, {sk} already existed · {source}")
                st.rerun()
        with col_bundled:
            if st.button("Re-seed built-in data"):
                with st.spinner("Loading..."):
                    ins, sk, source = seed_prices(use_live=False)
                st.success(f"Added {ins} new, {sk} already existed · {source}")
                st.rerun()

#Main columns
left_col, right_col = st.columns([1, 1.4])

with left_col:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-section">Add / update a price</div>', unsafe_allow_html=True)

    existing_items = [i['item_name'] for i in get_all_items()]
    item_input_mode = st.radio("Item", ["Type new", "Pick existing"], horizontal=True, label_visibility="collapsed")
    if item_input_mode == "Pick existing" and existing_items:
        item_name = st.selectbox("Select item", existing_items)
    else:
        item_name = st.text_input("Item name", placeholder="e.g. Chicken Biryani, Margherita Pizza")

    platform   = st.selectbox("Platform", ["Swiggy", "Zomato", "Dominos", "McDonalds", "EatClub", "EatSure", "Other"])
    restaurant = st.text_input("Restaurant (optional)", placeholder="e.g. Behrouz Biryani")
    price      = st.number_input("Price on this platform (₹)", min_value=0.0, value=0.0, step=5.0)

    if st.button("Add Price"):
        if not item_name or not str(item_name).strip():
            st.error("Please enter an item name.")
        elif price <= 0:
            st.error("Please enter a valid price.")
        else:
            try:
                add_price_entry(str(item_name).strip(), platform, restaurant.strip(), price)
                st.success(f"Saved ₹{price:,.0f} for {item_name} on {platform}!")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px;color:rgba(255,160,210,0.32);line-height:1.7;
         background:rgba(255,45,120,0.03);border-radius:10px;padding:12px 14px">
    💡 Tip: Add the same item on 2+ platforms to unlock the comparison.
    e.g. Chicken Biryani on Swiggy at ₹180, then on Zomato at ₹199.
    </div>""", unsafe_allow_html=True)

#Comparison view
with right_col:
    items = get_all_items()
    if items:
        item_names    = [i['item_name'] for i in items]
        selected_item = st.selectbox("Select item to compare", item_names)

        if selected_item:
            prices = get_item_prices(selected_item)

            if len(prices) >= 2:
                best      = prices[0]
                worst     = prices[-1]
                min_price = float(best['price'])
                max_price = float(worst['price'])
                saving    = max_price - min_price

                st.markdown(f"""
                <div class="winner-card">
                    <div class="winner-label">Cheapest option</div>
                    <div class="winner-platform">{best['platform']}</div>
                    <div class="winner-price">₹{min_price:,.0f}</div>
                    <div class="winner-saving">You save ₹{saving:,.0f} vs most expensive · {best['restaurant'] or 'Any restaurant'}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div style="font-size:12px;font-weight:600;color:rgba(255,120,180,0.35);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px">All platforms ranked</div>', unsafe_allow_html=True)

                for i, row in enumerate(prices):
                    p = float(row['price'])
                    if i == 0:
                        badge = '<span class="cr-badge badge-best">Cheapest </span>'
                        color = "#ff2d78"
                    elif i == len(prices) - 1:
                        extra = p - min_price
                        badge = f'<span class="cr-badge badge-worst">+₹{extra:,.0f} more</span>'
                        color = "rgba(255,160,210,0.4)"
                    else:
                        extra = p - min_price
                        badge = f'<span class="cr-badge badge-save">+₹{extra:,.0f}</span>'
                        color = "#ff6fae"

                    pill_html = pill(row['platform'])
                    col_info, col_price, col_del = st.columns([2.5, 1, 0.5])
                    with col_info:
                        st.markdown(f"""
                        <div style="padding:8px 0">
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">{pill_html} {badge}</div>
                            <div style="font-size:11px;color:rgba(255,160,210,0.3)">{row['restaurant'] or 'Any restaurant'} · Updated {row['last_updated']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_price:
                        st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:{color};padding-top:10px">₹{p:,.0f}</div>', unsafe_allow_html=True)
                    with col_del:
                        if st.button("✕", key=f"del_price_{selected_item}_{row['platform']}"):
                            delete_price_entry(selected_item, row['platform'])
                            st.rerun()
                    st.markdown('<hr style="margin:2px 0;border-color:rgba(255,45,120,0.05)">', unsafe_allow_html=True)

            elif len(prices) == 1:
                row  = prices[0]
                pill_html = pill(row['platform'])
                st.info(f"Only 1 platform for {selected_item}. Add more to compare!")
                st.markdown(f"""
                <div style="background:#2b1020;border:1px solid rgba(255,45,120,0.1);border-radius:12px;
                     padding:14px 18px;display:flex;align-items:center;justify-content:space-between">
                    <div>{pill_html}
                    <div style="font-size:11px;color:rgba(255,160,210,0.3);margin-top:4px">{row['restaurant'] or ''}</div>
                    </div>
                    <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#ff2d78">₹{float(row['price']):,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No items yet. Use the buttons above to load the dataset, or add your own!")

#All items grid 
st.markdown("---")
st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:1rem">All tracked items</div>', unsafe_allow_html=True)

items = get_all_items()
if items:
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            saving = float(item['max_price']) - float(item['min_price'])
            st.markdown(f"""
            <div class="item-card">
                <div class="item-name">{item['item_name']}</div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
                    <div class="item-meta">{item['platform_count']} platform{'s' if item['platform_count'] > 1 else ''}</div>
                    <div class="item-cheapest">₹{float(item['min_price']):,.0f}</div>
                </div>
                {f'<div style="font-size:11px;color:rgba(255,111,174,0.65);margin-top:4px">Save up to ₹{saving:,.0f}</div>' if saving > 0 else ''}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Add items using the form above to see them here.")

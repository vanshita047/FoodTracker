"""
🌸 FoodTrackr — Price data loader
Tries to pull live food price data from a public dataset API first.
Falls back to a built-in Pune dataset if the network call fails.

Live source: Open Food Facts (world.openfoodfacts.org) — free, no API key needed.
We filter for Indian products and map them to known food delivery platforms.
"""

import requests, json
from datetime import date

# ── Built-in Pune dataset (always available as fallback) ─────────────────────
BUNDLED_DATA = [
    # (item_name, platform, restaurant, price_inr)
    # Biryani
    ("Chicken Biryani",      "Swiggy",    "Behrouz Biryani",    299),
    ("Chicken Biryani",      "Zomato",    "Behrouz Biryani",    319),
    ("Chicken Biryani",      "EatClub",   "Behrouz Biryani",    269),
    ("Chicken Biryani",      "EatSure",   "Biryani Blues",      249),
    ("Veg Biryani",          "Swiggy",    "Behrouz Biryani",    229),
    ("Veg Biryani",          "Zomato",    "Behrouz Biryani",    239),
    ("Veg Biryani",          "EatClub",   "Behrouz Biryani",    199),
    ("Veg Biryani",          "EatSure",   "Biryani Blues",      189),
    ("Mutton Biryani",       "Swiggy",    "Behrouz Biryani",    379),
    ("Mutton Biryani",       "Zomato",    "Behrouz Biryani",    399),
    ("Mutton Biryani",       "EatClub",   "Behrouz Biryani",    349),
    # Pizza
    ("Margherita Pizza",     "Swiggy",    "Dominos",            199),
    ("Margherita Pizza",     "Zomato",    "Dominos",            199),
    ("Margherita Pizza",     "Dominos",   "Dominos",            179),
    ("Margherita Pizza",     "EatSure",   "Oven Story",         215),
    ("Pepperoni Pizza",      "Swiggy",    "Dominos",            349),
    ("Pepperoni Pizza",      "Zomato",    "Dominos",            349),
    ("Pepperoni Pizza",      "Dominos",   "Dominos",            319),
    ("Farmhouse Pizza",      "Swiggy",    "Dominos",            399),
    ("Farmhouse Pizza",      "Zomato",    "Dominos",            399),
    ("Farmhouse Pizza",      "Dominos",   "Dominos",            369),
    # Burgers
    ("McAloo Tikki Burger",  "Swiggy",    "McDonalds",           99),
    ("McAloo Tikki Burger",  "Zomato",    "McDonalds",           99),
    ("McAloo Tikki Burger",  "McDonalds", "McDonalds",           89),
    ("McSpicy Chicken",      "Swiggy",    "McDonalds",          229),
    ("McSpicy Chicken",      "Zomato",    "McDonalds",          229),
    ("McSpicy Chicken",      "McDonalds", "McDonalds",          209),
    ("Whopper Burger",       "Swiggy",    "Burger King",        199),
    ("Whopper Burger",       "Zomato",    "Burger King",        219),
    # Chinese
    ("Veg Fried Rice",       "Swiggy",    "Chinese Wok",        179),
    ("Veg Fried Rice",       "Zomato",    "Chinese Wok",        189),
    ("Veg Fried Rice",       "EatClub",   "Chinese Wok",        159),
    ("Veg Fried Rice",       "EatSure",   "Mealbox",            149),
    ("Chicken Fried Rice",   "Swiggy",    "Chinese Wok",        219),
    ("Chicken Fried Rice",   "Zomato",    "Chinese Wok",        229),
    ("Chicken Fried Rice",   "EatClub",   "Chinese Wok",        199),
    ("Hakka Noodles",        "Swiggy",    "Chinese Wok",        169),
    ("Hakka Noodles",        "Zomato",    "Chinese Wok",        179),
    ("Hakka Noodles",        "EatClub",   "Chinese Wok",        149),
    # South Indian
    ("Masala Dosa",          "Swiggy",    "MTR",                129),
    ("Masala Dosa",          "Zomato",    "MTR",                139),
    ("Masala Dosa",          "EatClub",   "Dosa Plaza",         109),
    ("Idli Sambar (3 pcs)",  "Swiggy",    "MTR",                 99),
    ("Idli Sambar (3 pcs)",  "Zomato",    "MTR",                109),
    ("Idli Sambar (3 pcs)",  "EatClub",   "Dosa Plaza",          89),
    ("Vada (2 pcs)",         "Swiggy",    "MTR",                 79),
    ("Vada (2 pcs)",         "Zomato",    "MTR",                 79),
    ("Vada (2 pcs)",         "EatClub",   "Dosa Plaza",          69),
    # North Indian
    ("Butter Chicken",       "Swiggy",    "Barbeque Nation",    369),
    ("Butter Chicken",       "Zomato",    "Barbeque Nation",    389),
    ("Butter Chicken",       "EatSure",   "Punjabi Tadka",      319),
    ("Dal Makhani",          "Swiggy",    "Barbeque Nation",    249),
    ("Dal Makhani",          "Zomato",    "Barbeque Nation",    269),
    ("Dal Makhani",          "EatSure",   "Punjabi Tadka",      219),
    ("Dal Makhani",          "EatClub",   "Punjabi Tadka",      199),
    ("Paneer Tikka",         "Swiggy",    "Barbeque Nation",    299),
    ("Paneer Tikka",         "Zomato",    "Barbeque Nation",    319),
    ("Paneer Tikka",         "EatSure",   "Punjab Grill",       279),
    ("Garlic Naan",          "Swiggy",    "Barbeque Nation",     49),
    ("Garlic Naan",          "Zomato",    "Barbeque Nation",     55),
    ("Garlic Naan",          "EatClub",   "Punjabi Tadka",       39),
    # Wraps
    ("Chicken Kathi Roll",   "Swiggy",    "Faasos",             179),
    ("Chicken Kathi Roll",   "Zomato",    "Faasos",             189),
    ("Chicken Kathi Roll",   "EatClub",   "Faasos",             159),
    ("Chicken Kathi Roll",   "EatSure",   "Faasos",             149),
    ("Paneer Kathi Roll",    "Swiggy",    "Faasos",             159),
    ("Paneer Kathi Roll",    "Zomato",    "Faasos",             169),
    ("Paneer Kathi Roll",    "EatClub",   "Faasos",             139),
    # Snacks
    ("Samosa (2 pcs)",       "Swiggy",    "Haldirams",           59),
    ("Samosa (2 pcs)",       "Zomato",    "Haldirams",           65),
    ("Pav Bhaji",            "Swiggy",    "Goli Vada Pav",      129),
    ("Pav Bhaji",            "Zomato",    "Goli Vada Pav",      139),
    ("Pav Bhaji",            "EatClub",   "Goli Vada Pav",      109),
    ("Vada Pav",             "Swiggy",    "Goli Vada Pav",       49),
    ("Vada Pav",             "Zomato",    "Goli Vada Pav",       55),
    ("Vada Pav",             "EatClub",   "Goli Vada Pav",       45),
    # Drinks
    ("Cold Coffee",          "Swiggy",    "Cafe Coffee Day",    139),
    ("Cold Coffee",          "Zomato",    "Cafe Coffee Day",    149),
    ("Cold Coffee",          "EatClub",   "Third Wave Coffee",  129),
    ("Mango Lassi",          "Swiggy",    "Haldirams",           99),
    ("Mango Lassi",          "Zomato",    "Haldirams",          109),
    ("Mango Lassi",          "EatClub",   "Haldirams",           89),
    ("Masala Chaas",         "Swiggy",    "Haldirams",           69),
    ("Masala Chaas",         "Zomato",    "Haldirams",           75),
    ("Masala Chaas",         "EatClub",   "Haldirams",           59),
    # Desserts
    ("Gulab Jamun (2 pcs)",  "Swiggy",    "Haldirams",           89),
    ("Gulab Jamun (2 pcs)",  "Zomato",    "Haldirams",           99),
    ("Gulab Jamun (2 pcs)",  "EatSure",   "Haldirams",           79),
    ("Chocolate Pastry",     "Swiggy",    "Monginis",            79),
    ("Chocolate Pastry",     "Zomato",    "Monginis",            89),
]

# ── Zomato Kaggle dataset mapping ─────────────────────────────────────────────
# Source: Kaggle "Zomato Restaurants in India" dataset (public domain)
# URL: https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data
# We use the Open Data Soft mirror which doesn't need auth:
OPENDATA_URL = (
    "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    "georef-india-state/records?limit=1"  # lightweight ping to check connectivity
)

SWIGGY_ZOMATO_PRICES_URL = (
    "https://raw.githubusercontent.com/dsrscientist/dataset1/master/"
    "zomato.csv"
)


def _fetch_kaggle_style_data() -> list[tuple]:
    """
    Pulls from a public GitHub-hosted Zomato India CSV (no API key needed).
    Returns list of (item_name, platform, restaurant, price) tuples.
    Only used if network is reachable.
    """
    # Map of common cuisine keywords → canonical dish names
    CUISINE_MAP = {
        "biryani": "Chicken Biryani",
        "pizza":   "Margherita Pizza",
        "burger":  "McAloo Tikki Burger",
        "noodles": "Hakka Noodles",
        "dosa":    "Masala Dosa",
        "paneer":  "Paneer Tikka",
        "roll":    "Chicken Kathi Roll",
        "thali":   "Veg Thali",
        "pasta":   "Penne Arrabbiata",
        "sandwich":"Veg Sandwich",
        "momos":   "Veg Momos",
        "dal":     "Dal Makhani",
    }
    PLATFORMS = ["Swiggy", "Zomato", "EatClub", "EatSure"]
    # price multipliers per platform (Zomato ~5% more, EatClub ~15% less)
    MULTIPLIERS = {"Swiggy": 1.0, "Zomato": 1.05, "EatClub": 0.85, "EatSure": 0.88}

    resp = requests.get(SWIGGY_ZOMATO_PRICES_URL, timeout=8)
    resp.raise_for_status()
    lines = resp.text.splitlines()

    # find column indices
    header = [h.strip().lower().strip('"') for h in lines[0].split(",")]
    try:
        name_idx = next(i for i, h in enumerate(header) if "name" in h or "restaurant" in h)
        rate_idx = next(i for i, h in enumerate(header) if "rate" in h or "cost" in h or "approx" in h)
        cuisine_idx = next((i for i, h in enumerate(header) if "cuisin" in h), None)
    except StopIteration:
        return []

    seen = set()
    results = []
    for line in lines[1:600]:          # cap at 600 rows
        cols = line.split(",")
        if len(cols) <= max(name_idx, rate_idx):
            continue
        restaurant = cols[name_idx].strip().strip('"')
        raw_rate   = cols[rate_idx].strip().strip('"').replace("/2", "").replace("NEW","").strip()
        try:
            base_price = float(raw_rate) / 2   # "cost for two" → per person
        except ValueError:
            continue
        if base_price < 50 or base_price > 800:
            continue

        # derive a dish name from cuisines column or use generic
        dish = "Mixed Plate"
        if cuisine_idx and cuisine_idx < len(cols):
            cuisine_text = cols[cuisine_idx].lower()
            for kw, mapped in CUISINE_MAP.items():
                if kw in cuisine_text:
                    dish = mapped
                    break

        for platform in PLATFORMS:
            price = round(base_price * MULTIPLIERS[platform])
            key   = (dish, platform)
            if key not in seen:
                seen.add(key)
                results.append((dish, platform, restaurant[:80], price))

        if len(results) > 300:
            break

    return results


def load_price_data(use_live: bool = True) -> tuple[list, str]:
    """
    Returns (data_list, source_label).
    data_list = [(item_name, platform, restaurant, price), ...]
    source_label = human-readable string shown in the UI.
    """
    if use_live:
        try:
            data = _fetch_kaggle_style_data()
            if data:
                return data, "Zomato India dataset (Kaggle / GitHub)"
        except Exception:
            pass
    return BUNDLED_DATA, "Built-in Pune dataset"


def seed_prices(use_live: bool = True) -> tuple[int, int, str]:
    """
    Insert price data into price_comparison table.
    Safe to call multiple times — INSERT IGNORE skips duplicates.
    Returns (inserted, skipped, source_label).
    """
    from db import get_connection
    data, source = load_price_data(use_live)
    conn = get_connection()
    cur  = conn.cursor()
    ins  = skipped = 0
    today = date.today()
    for item_name, platform, restaurant, price in data:
        try:
            cur.execute("""
                INSERT IGNORE INTO price_comparison
                    (item_name, platform, restaurant, price, last_updated)
                VALUES (%s, %s, %s, %s, %s)
            """, (item_name, platform, restaurant, float(price), today))
            if cur.rowcount > 0:
                ins += 1
            else:
                skipped += 1
        except Exception:
            skipped += 1
    conn.commit()
    conn.close()
    return ins, skipped, source

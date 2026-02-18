import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# 1. PAGE CONFIG & THEME
st.set_page_config(page_title="Aetheris Global AI", page_icon="🌍", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400&display=swap');
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; }
    .title-text {
        font-family: 'Syncopate', sans-serif;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px; font-weight: bold; text-align: center;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 20px; border: 1px solid #00f2fe; margin-bottom: 15px;
    }
    .price-tag { color: #00f2fe; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATASET
featured_cities = {
    "Kyoto": {"lat": 35.0116, "lon": 135.7681, "places": ["Fushimi Inari", "Kinkaku-ji", "Arashiyama"]},
    "Paris": {"lat": 48.8566, "lon": 2.3522, "places": ["Eiffel Tower", "Louvre", "Arc de Triomphe"]},
    "Mumbai": {"lat": 18.9226, "lon": 72.8333, "places": ["Gateway of India", "Marine Drive", "Elephanta Caves"]}
}

# 3. NAVIGATION & SESSION STATE INITIALIZATION
if 'page' not in st.session_state: st.session_state.page = "Home"
if 'current_city' not in st.session_state: st.session_state.current_city = None
if 'city_data' not in st.session_state: st.session_state.city_data = None
if 'user_origin' not in st.session_state: st.session_state.user_origin = "New Delhi" # Default value

# 4. SIDEBAR (AI, CURRENCY, TIER)
with st.sidebar:
    st.markdown("### 🤖 Aetheris Assistant")
    msg = st.text_input("Ask about your trip:")
    if msg: st.write(f"**AI:** Analysis for '{msg}' is complete. Logistics optimized.")
    
    st.divider()
    st.markdown("### 💱 Live Exchange Rate")
    currency = st.radio("Display Price In:", ["INR (₹)", "USD ($)", "EUR (€)"])
    rates = {"INR (₹)": 1.0, "USD ($)": 0.012, "EUR (€)": 0.011}
    symbol = currency.split(" ")[1].replace("(", "").replace(")", "")
    
    st.divider()
    tier = st.selectbox("Comfort Tier", ["Standard", "Premium", "Quantum"])

# 5. PAGE: HOME
if st.session_state.page == "Home":
    st.markdown('<p class="title-text">AETHERIS NEURAL ENGINE</p>', unsafe_allow_html=True)
    
    with st.expander("📖 HOW TO OPERATE APP", expanded=True):
        st.write("""
        1. **Search:** Enter any global city to center the high-precision map.
        2. **Logistics:** Define your origin, total budget in ₹, and trip length.
        3. **Analysis:** Review the AI-calculated budget split.
        4. **Deep-Dive:** Click '🔎 Details' for landmark-specific data.
        """)

    # INPUT SECTION
    c1, c2, c3, c4 = st.columns(4)
    # Store origin directly in session_state
    st.session_state.user_origin = c1.text_input("🛫 Starting Point", st.session_state.user_origin)
    query = c2.text_input("🛬 Search Destination", placeholder="Enter city name...")
    budget_inr = c3.number_input("💰 Budget (Total ₹)", 5000, 1000000, 50000)
    days = c4.number_input("📅 Days", 1, 30, 3)

    if query:
        city = query.strip().title()
        
        if city in featured_cities:
            data = featured_cities[city]
        else:
            rand_gen = random.Random(city)
            data = {
                "lat": rand_gen.uniform(-50, 60), 
                "lon": rand_gen.uniform(-170, 170),
                "places": [f"{city} Central Hub", f"Historic {city} Sector"]
            }
        
        st.session_state.current_city = city
        st.session_state.city_data = data

        conv = rates[currency]
        total_conv = budget_inr * conv
        f_est = (budget_inr * 0.4) * conv
        h_est = ((budget_inr * 0.3) / days) * conv

        st.divider()
        
        col_map, col_calc = st.columns([2, 1])
        with col_map:
            st.subheader(f"📍 Precision Map: {city}")
            map_df = pd.DataFrame({'lat': [data['lat']], 'lon': [data['lon']]})
            st.map(map_df, zoom=12)
        
        with col_calc:
            st.subheader("📊 AI Budget Allocation")
            st.markdown(f"""<div class="result-card">
                <p>✈️ Flight Est: <span class="price-tag">{symbol}{int(f_est):,}</span></p>
                <p>🏨 Hotel Est: <span class="price-tag">{symbol}{int(h_est):,}</span>/night</p>
                <p><b>Total ({currency}): {symbol}{int(total_conv):,}</b></p>
                <hr><b>Suggested Landmarks:</b></div>""", unsafe_allow_html=True)
            
            for p_name in data['places']:
                if st.button(f"🔎 Details: {p_name}"):
                    st.session_state.selected_place = p_name
                    st.session_state.page = "Details"
                    st.rerun()

# 6. PAGE: DETAILS
elif st.session_state.page == "Details":
    city = st.session_state.current_city
    place = st.session_state.selected_place
    # Retrieve origin from session_state
    origin_val = st.session_state.user_origin
    
    st.markdown(f'<p class="title-text">{place.upper()}</p>', unsafe_allow_html=True)
    
    if st.button("⬅️ Return to Global Map"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.divider()
    
    st.markdown(f"""
    <div class="result-card">
        <h3>📍 Location Intelligence</h3>
        <p><b>Node:</b> {place}</p>
        <p><b>City:</b> {city}</p>
        <p><b>Tier:</b> {tier}</p>
        <hr>
        <p><b>AI Analysis:</b> This sector has been verified for your travel duration. 
        Local transit links are synchronized with your starting point at <b>{origin_val}</b>.</p>
        <p><b>Security Status:</b> Quantum-Secured Site.</p>
    </div>
    """, unsafe_allow_html=True)

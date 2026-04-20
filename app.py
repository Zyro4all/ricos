import streamlit as st
import pandas as pd
import requests
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide", page_icon="💀")

# --- 1. PASTE YOUR NEW LINK HERE ---
CSV_URL = "PASTE_YOUR_NEW_CSV_LINK_HERE"

# --- 2. THE FORM URL (Pre-filled for you) ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScMaWmzPd-VnCu75dkYn-DYqPSgmyfcEC_uC-10E1sRD-BfSg/formResponse"

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load data with a cache-buster to ensure it's always fresh
try:
    # This random number forces Google to show the newest data immediately
    refresh_url = f"{CSV_URL}&nocache={random.randint(1, 100000)}"
    df = pd.read_csv(refresh_url)
    # Ensure we only care about Name and Key columns
    df = df[['Name', 'Key']]
except Exception as e:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate New Key")
    u_name = st.text_input("Customer Name", placeholder="e.g. John Doe")
    tier = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Save to Cloud", use_container_width=True):
        if u_name:
            # Create Key
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[tier]
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_key = f"RICOS-{prefix}-{rand_str}"
            
            # Send to Google Form
            payload = {
                "entry.1278795252": u_name, 
                "entry.1557051665": new_key
            }
            
            try:
                requests.post(FORM_URL, data=payload)
                st.success(f"Successfully Created: {new_key}")
                st.balloons()
                st.info("Wait 5-10 seconds for the database to sync, then refresh.")
            except:
                st.error("Connection error. Please try again.")
        else:
            st.error("Please enter a name first!")

with col2:
    st.subheader("Live Database")
    st.dataframe(df, use_container_width=True, height=400)
    if st.button("🔄 Refresh Table", use_container_width=True):
        st.rerun()

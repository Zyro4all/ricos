import streamlit as st
import pandas as pd
import requests
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide", page_icon="💀")

# --- YOUR CUSTOM LINKS ---
# The new link you just gave me
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-3ni_JieyfjhMrwxKeSI2seJBb9xWPEfNPpiw1I09EkivalS4uAA6Sfy-S18Gs5Xgl9ICFHTmT5mS/pub?output=csv"

# Your Form submission link
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScMaWmzPd-VnCu75dkYn-DYqPSgmyfcEC_uC-10E1sRD-BfSg/formResponse"

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load data with a 'cache-buster' so it doesn't show old data
try:
    # Adding a random number to the URL forces Google to refresh the data
    refresh_url = f"{CSV_URL}&nocache={random.randint(1, 100000)}"
    df = pd.read_csv(refresh_url)
    
    # If the sheet has a Timestamp column from the form, we skip it
    if 'Timestamp' in df.columns:
        df = df.drop(columns=['Timestamp'])
except Exception:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate New Key")
    u_name = st.text_input("Customer Name")
    tier = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Save to Cloud", use_container_width=True):
        if u_name:
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[tier]
            new_key = f"RICOS-{prefix}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
            
            # Send to your Google Form
            payload = {
                "entry.1278795252": u_name, 
                "entry.1557051665": new_key
            }
            
            try:
                requests.post(FORM_URL, data=payload)
                st.success(f"Successfully Created: {new_key}")
                st.info("Wait 10 seconds, then click Refresh Table.")
            except:
                st.error("Connection error.")
        else:
            st.error("Please enter a name!")

with col2:
    st.subheader("Live Database")
    st.dataframe(df, use_container_width=True, height=400)
    if st.button("🔄 Refresh Table", use_container_width=True):
        st.rerun()

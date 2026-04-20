import streamlit as st
import pandas as pd
import requests
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# --- THE LINKS ---
# This is the link you just sent me
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSiZQMUDlM2wFrShtweDCgyTVkio04jMNX35Z-HUa35GasTfaPu-H7pNb_gQHSTLOqXeFAVMLBzQKc9/pub?output=csv"

# This is your Form ID from earlier
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScMaWmzPd-VnCu75dkYn-DYqPSgmyfcEC_uC-10E1sRD-BfSg/formResponse"

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load data
try:
    # We add a random number to the URL so it doesn't show old, cached data
    df = pd.read_csv(f"{CSV_URL}&refresh={random.randint(1,1000)}")
except:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate & Save")
    u_name = st.text_input("Customer Name")
    tier = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Save"):
        if u_name:
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[tier]
            new_key = f"RICOS-{prefix}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
            
            # --- SEND TO GOOGLE FORM ---
            payload = {
                "entry.1278795252": u_name, 
                "entry.1557051665": new_key
            }
            
            try:
                requests.post(FORM_URL, data=payload)
                st.success(f"Key Saved: {new_key}")
                st.info("Wait 10 seconds, then click Refresh.")
            except:
                st.error("Submission failed.")
        else:
            st.error("Enter a name!")

with col2:
    st.subheader("Live Database")
    # We only show the Name and Key columns to keep it clean
    if not df.empty:
        st.dataframe(df[["Name", "Key"]], use_container_width=True)
    else:
        st.write("No keys found yet. Try generating one!")
        
    if st.button("Refresh Table"):
        st.rerun()

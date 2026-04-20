import streamlit as st
import pandas as pd
import requests
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# The URL from your Secrets
SHEET_URL = st.secrets["spreadsheet_url"]
# This is your Public CSV link for READING data (from Image 2)
CSV_URL = "https://docs.google.com/spreadsheets/d/1VByNd7cFDO62STXib2h8s1L4YTyfmxygcymCOMBeAvE/edit?usp=sharing"

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load data simply using pandas
try:
    df = pd.read_csv(CSV_URL)
except:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate New Key")
    u_name = st.text_input("Customer Name")
    tier = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    st.info("To save: Copy the key below and paste it into your Google Sheet manually for now, or use the 'Form' method.")
    
    if st.button("Generate Key"):
        if u_name:
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[tier]
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_key = f"RICOS-{prefix}-{rand}"
            
            st.success("Key Generated!")
            st.code(new_key)
            st.warning("Since Google is blocking the auto-save, please paste this into row " + str(len(df)+2) + " of your sheet.")
        else:
            st.error("Enter a name!")

with col2:
    st.subheader("Live Database (Refresh to update)")
    st.dataframe(df, use_container_width=True)
    if st.button("Refresh Table"):
        st.rerun()

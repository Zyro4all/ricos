import streamlit as st
import pandas as pd
import requests
import random
import string
import time

st.set_page_config(page_title="RICOS ADMIN", layout="wide", page_icon="💀")

# --- YOUR LINKS ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-3ni_JieyfjhMrwxKeSI2seJBb9xWPEfNPpiw1I09EkivalS4uAA6Sfy-S18Gs5Xgl9ICFHTmT5mS/pub?output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScMaWmzPd-VnCu75dkYn-DYqPSgmyfcEC_uC-10E1sRD-BfSg/formResponse"
SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1VByNd7cFDO62STXib2h8s1L4YTyfmxygcymCOMBeAvE/edit"

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load data
try:
    refresh_url = f"{CSV_URL}&nocache={random.randint(1, 100000)}"
    df = pd.read_csv(refresh_url)
    if 'Timestamp' in df.columns:
        df = df.drop(columns=['Timestamp'])
except Exception:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate Keys")
    u_name = st.text_input("Customer Name (or Batch Name)")
    tier = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    # --- ADDED QUANTITY INPUT ---
    num_to_gen = st.number_input("Quantity to generate", min_value=1, max_value=50, value=1)
    
    if st.button(f"🚀 Generate {num_to_gen} Key(s)", use_container_width=True):
        if u_name:
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[tier]
            
            success_count = 0
            progress_bar = st.progress(0)
            
            # --- LOOP FOR MULTIPLE KEYS ---
            for i in range(num_to_gen):
                # Unique key for each iteration
                new_key = f"RICOS-{prefix}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
                payload = {"entry.1278795252": u_name, "entry.1557051665": new_key}
                
                try:
                    requests.post(FORM_URL, data=payload)
                    success_count += 1
                except:
                    st.error(f"Failed to save key {i+1}")
                
                # Update progress
                progress_bar.progress((i + 1) / num_to_gen)
            
            if success_count > 0:
                st.success(f"Successfully generated {success_count} keys for {u_name}!")
                time.sleep(1) # Small delay to let Google Sheet update
                st.rerun()
        else:
            st.error("Enter a name!")

    st.divider()
    st.subheader("Manage Data")
    st.link_button("🗑️ Open Database to Delete Keys", SHEET_EDIT_URL, use_container_width=True)

with col2:
    st.subheader("Live Database")
    st.dataframe(df, use_container_width=True, height=500)
    if st.button("🔄 Refresh Table", use_container_width=True):
        st.rerun()

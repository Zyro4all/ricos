import streamlit as st
import pandas as pd
import random
import string

# Your actual published CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSiZQMUDlM2wFrShtweDCgyTVkio04jMNX35Z-HUa35GasTfaPu-H7pNb_gQHSTLOqXeFAVMLBzQKc9/pub?output=csv"

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

st.title("💀 RICOS SNIPER | ADMIN PANEL")

# Function to load the data from the web link
def load_data():
    try:
        return pd.read_csv(CSV_URL)
    except:
        return pd.DataFrame(columns=["Name", "Key"])

df = load_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Generate Key")
    user_name = st.text_input("User Name / Discord")
    
    if st.button("Generate New Key"):
        if user_name:
            new_key = f"RICOS-LT-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
            st.success(f"Key Generated for {user_name}:")
            st.code(new_key)
            st.warning("⚠️ Manual Step: Copy this key and paste it into your Google Sheet row.")
        else:
            st.error("Enter a name first!")

with col2:
    st.subheader("Current Database (Read Only)")
    st.dataframe(df, use_container_width=True)
    if st.button("Refresh List"):
        st.rerun()

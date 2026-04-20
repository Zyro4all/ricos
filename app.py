import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# This connects to your Google Sheet via the URL
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load existing data
try:
    df = conn.read()
    # If sheet is empty, create the structure
    if df.empty:
        df = pd.DataFrame(columns=["Name", "Key"])
except:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Generate New Key")
    user_name = st.text_input("User Name / Discord ID")
    if st.button("Generate & Save"):
        if user_name:
            # Create the key
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_key = f"RICOS-LT-{random_str}"
            
            # Update the dataframe
            new_row = pd.DataFrame([{"Name": user_name, "Key": new_key}])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Push back to Google Sheets
            conn.update(data=df)
            st.success(f"Key saved to Cloud: {new_key}")
        else:
            st.error("Please enter a name first!")

with col2:
    st.subheader("Key Database (Cloud)")
    st.dataframe(df, use_container_width=True)

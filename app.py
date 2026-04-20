import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# Connect to the NEW sheet link provided
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Safe Read
try:
    df = conn.read(ttl=0)
except Exception:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate Key")
    user_name = st.text_input("Customer Name")
    duration = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Auto-Save"):
        if user_name:
            # Match Sniper Logic
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[duration]
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_key = f"RICOS-{prefix}-{rand}"
            
            # Add to dataframe
            new_row = pd.DataFrame([{"Name": user_name, "Key": new_key}])
            updated_df = pd.concat([df, new_row], ignore_index=True) if not df.empty else new_row
            
            # Update Google Sheets
            try:
                conn.update(data=updated_df)
                st.success(f"Saved: {new_key}")
                st.rerun()
            except Exception as e:
                st.error("Permission Error: Did you update the link in your Streamlit Secrets?")
        else:
            st.error("Enter a name first!")

with col2:
    st.subheader("Cloud Database")
    st.dataframe(df, use_container_width=True)

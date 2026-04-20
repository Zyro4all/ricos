import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# Connect using the PRIVATE link from Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load existing keys
try:
    # Use ttl=0 to always get the freshest keys from the sheet
    df = conn.read(ttl=0)
except Exception:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate New Key")
    user_name = st.text_input("Customer Name / Discord ID")
    
    # Tier selector for your Sniper logic
    duration = st.selectbox("Key Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Auto-Save"):
        if user_name:
            # Match the prefixes your Sniper script expects
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[duration]
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            new_key = f"RICOS-{prefix}-{rand_str}"
            
            # Update the Sheet
            new_row = pd.DataFrame([{"Name": user_name, "Key": new_key}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Push to Google Sheets (Requires Private Link in Secrets)
            conn.update(data=updated_df)
            
            st.success(f"Key saved to Cloud!")
            st.code(new_key)
        else:
            st.error("Please enter a name!")

with col2:
    st.subheader("Current Keys")
    st.dataframe(df, use_container_width=True)

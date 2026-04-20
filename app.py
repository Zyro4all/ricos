import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# 1. Establish connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# 2. Safe Read with cache clearing
try:
    df = conn.read(ttl=0)
except Exception as e:
    st.warning("Sheet is currently empty or connecting...")
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate New Key")
    user_name = st.text_input("Customer Name")
    duration = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Auto-Save"):
        if user_name:
            # Create Key
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[duration]
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_key = f"RICOS-{prefix}-{rand}"
            
            # Prepare data
            new_row = pd.DataFrame([{"Name": user_name, "Key": new_key}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # 3. The Update (Requires "Editor" permission on the sheet)
            try:
                conn.update(data=updated_df)
                st.success(f"Successfully saved: {new_key}")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error("STILL NO PERMISSION: You must click 'Share' in Google Sheets and set 'Anyone with the link' to 'EDITOR'.")
        else:
            st.error("Please enter a name!")

with col2:
    st.subheader("Live Database")
    st.dataframe(df, use_container_width=True)

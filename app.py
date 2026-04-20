import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# Connect using the Secret link
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Load existing data
try:
    df = conn.read()
except:
    df = pd.DataFrame(columns=["Name", "Key"])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate New Key")
    user_name = st.text_input("Customer Name")
    
    # Duration Selector added
    duration = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Auto-Save"):
        if user_name:
            # Create Key based on Tier
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[duration]
            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            new_key = f"RICOS-{prefix}-{rand}"
            
            # Add to dataframe and push to Google Sheets
            new_row = pd.DataFrame([{"Name": user_name, "Key": new_key}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            conn.update(data=updated_df)
            st.success(f"Successfully saved to Google Sheets!")
            st.code(new_key)
        else:
            st.error("Enter a name first!")

with col2:
    st.subheader("Live Database")
    st.dataframe(df, use_container_width=True)

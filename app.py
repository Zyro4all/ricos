import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string

st.set_page_config(page_title="RICOS ADMIN", layout="wide", page_icon="💀")

st.title("💀 RICOS SNIPER | CLOUD ADMIN")

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Load existing data
df = conn.read(ttl=0) # ttl=0 ensures we always get the freshest data

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate New Key")
    u_name = st.text_input("Customer Name")
    tier = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("🚀 Generate & Save", use_container_width=True):
        if u_name:
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[tier]
            new_key = f"RICOS-{prefix}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
            
            # Add new data to the dataframe
            new_row = pd.DataFrame([{"Name": u_name, "Key": new_key}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Update the Google Sheet
            conn.update(data=updated_df)
            st.success(f"Saved: {new_key}")
            st.rerun()
        else:
            st.error("Enter a name!")

with col2:
    st.subheader("Live Database")
    
    if not df.empty:
        # We create a table with a delete button for each row
        for index, row in df.iterrows():
            c1, c2, c3 = st.columns([2, 3, 1])
            c1.write(row['Name'])
            c2.code(row['Key'])
            if c3.button("🗑️", key=f"delete_{index}"):
                # Remove the row and update the sheet
                df = df.drop(index)
                conn.update(data=df)
                st.toast(f"Deleted key for {row['Name']}")
                st.rerun()
    else:
        st.write("No keys found.")

    if st.button("🔄 Force Refresh", use_container_width=True):
        st.rerun()

import streamlit as st
import json
import os
import random
import string

# Use a fixed filename to ensure the Sniper and Admin stay synced
DB_FILE = "keys_database.json"

def load_data():
    """Robust data loading to prevent overwriting with empty data."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                # Ensure the core structure exists
                if "keys" not in data: data["keys"] = {}
                if "names" not in data: data["names"] = {}
                if "owner_key" not in data: data["owner_key"] = "RICOS-OWNER-ADMIN-999"
                return data
        except:
            pass
    # Return fresh template only if file is missing or totally broken
    return {"keys": {}, "names": {}, "owner_key": "RICOS-OWNER-ADMIN-999"}

def save_data(data):
    """Force write data to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- UI SETTINGS ---
st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# Tactical Red/Black Theme
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { width: 100%; background-color: #ff0000; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #aa0000; border: 1px solid white; }
    .stTextInput>div>div>input { background-color: #111; color: white; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("💀 RICOS SNIPER | ADMIN PANEL")

# Initialize data
data = load_data()

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Generate Key")
    with st.container():
        user_name = st.text_input("Name / Discord", placeholder="User Name")
        duration = st.selectbox("Tier", ["1 Day", "1 Week", "1 Month", "Lifetime"])
        
        if st.button("SAVE KEY TO DATABASE"):
            # Key Logic
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[duration]
            rand_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_key = f"RICOS-{prefix}-{rand_part}"
            days_val = {"1 Day": 1, "1 Week": 7, "1 Month": 30, "Lifetime": 9999}[duration]
            
            # Update local data object
            data["keys"][new_key] = days_val
            data["names"][new_key] = user_name if user_name else "Unknown"
            
            # Force write to keys_database.json
            save_data(data)
            
            st.success(f"Success! Key added to {DB_FILE}")
            st.code(new_key)

with col2:
    st.subheader("Database Management")
    
    if not data["keys"]:
        st.info("Database is currently empty.")
    else:
        # Loop through keys to allow deletion and naming
        for key in list(data["keys"].keys()):
            name = data["names"].get(key, "N/A")
            tier = data["keys"][key]
            
            with st.expander(f"👤 {name} ({key})"):
                c1, c2 = st.columns([3, 1])
                c1.write(f"**Key:** `{key}`")
                c1.write(f"**Days:** {tier}")
                
                if c2.button("DELETE", key=f"del_{key}"):
                    # Remove from both dictionaries
                    if key in data["keys"]: del data["keys"][key]
                    if key in data["names"]: del data["names"][key]
                    
                    # Force save the updated (shorter) list
                    save_data(data)
                    st.rerun()

# Verification Footer
st.divider()
st.write("### Live File View")
st.json(data)

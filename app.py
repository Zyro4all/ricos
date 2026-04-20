import streamlit as st
import json
import os
import random
import string

# Ensure the file is saved in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "keys_database.json")

def load_data():
    """Load data from JSON or create a fresh template if missing/corrupt."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                # Ensure all required structures exist
                if "keys" not in data: data["keys"] = {}
                if "names" not in data: data["names"] = {}
                if "owner_key" not in data: data["owner_key"] = "RICOS-OWNER-ADMIN-999"
                return data
        except (json.JSONDecodeError, Exception):
            pass
    
    # Default template if file doesn't exist
    return {"keys": {}, "names": {}, "owner_key": "RICOS-OWNER-ADMIN-999"}

def save_data(data):
    """Save the dictionary to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- UI CONFIG ---
st.set_page_config(page_title="RICOS ADMIN", layout="wide")

# Custom CSS for the "Skull" aesthetic
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff0000; color: white; border: none; }
    .stButton>button:hover { background-color: #880000; border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

st.title("💀 RICOS SNIPER | MASTER ADMIN")
st.write(f"**Database Location:** `{DB_FILE}`")

data = load_data()

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🛠️ Generate New Key")
    with st.container(border=True):
        user_name = st.text_input("User Name / Discord ID", placeholder="e.g. Rico#0001")
        duration = st.selectbox("Tier / Duration", ["1 Day", "1 Week", "1 Month", "Lifetime"])
        
        if st.button("GENERATE & SAVE KEY"):
            # Create the key string
            prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[duration]
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_key = f"RICOS-{prefix}-{random_str}"
            
            # Map duration days for the checker logic
            days_map = {"1 Day": 1, "1 Week": 7, "1 Month": 30, "Lifetime": 9999}
            
            # Save to local data object
            data["keys"][new_key] = days_map[duration]
            data["names"][new_key] = user_name if user_name else "Unknown User"
            
            # Write to file
            save_data(data)
            
            st.success(f"Key Generated Successfully!")
            st.code(new_key)
            st.balloons()

with col2:
    st.subheader("📋 Active Key Database")
    
    if not data["keys"]:
        st.info("No keys found in database. Generate one to get started.")
    else:
        # We use list(data["keys"].keys()) so we can delete while looping
        for key in list(data["keys"].keys()):
            name = data["names"].get(key, "N/A")
            days = data["keys"][key]
            
            with st.expander(f"👤 {name} | {key}"):
                c1, c2 = st.columns([3, 1])
                c1.write(f"**Key:** `{key}`")
                c1.write(f"**Duration:** {days} Days")
                
                if c2.button("DELETE", key=f"del_{key}"):
                    del data["keys"][key]
                    if key in data["names"]:
                        del data["names"][key]
                    save_data(data)
                    st.rerun()

# --- DEBUG SECTION ---
st.divider()
with st.expander("🔍 View Raw keys_database.json"):
    st.json(data)

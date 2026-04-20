import streamlit as st
import json, os, random, string

DB_FILE = "keys_database.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"keys": {}, "names": {}, "owner_key": "RICOS-OWNER-ADMIN-999"}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

st.set_page_config(page_title="RICOS ADMIN", layout="wide")
st.title("💀 RICOS SNIPER ADMIN PANEL")

data = load_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Generate New Key")
    user_name = st.text_input("User Name / Discord")
    duration = st.selectbox("Duration", ["1 Day", "1 Week", "1 Month", "Lifetime"])
    
    if st.button("Generate & Save"):
        prefix = {"1 Day": "1D", "1 Week": "1W", "1 Month": "1M", "Lifetime": "LT"}[duration]
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        new_key = f"RICOS-{prefix}-{random_str}"
        
        # Save to database
        data["keys"][new_key] = duration
        data["names"][new_key] = user_name if user_name else "Unknown"
        save_data(data)
        st.success(f"Generated: {new_key}")
        st.code(new_key)

with col2:
    st.subheader("Key Database")
    if not data["keys"]:
        st.info("No active keys found.")
    else:
        for key, dur in list(data["keys"].items()):
            name = data["names"].get(key, "N/A")
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.text(f"👤 {name}\n🔑 {key}")
            c2.text(f"⏳ {dur}")
            if c3.button("DELETE", key=f"del_{key}"):
                del data["keys"][key]
                if key in data["names"]: del data["names"][key]
                save_data(data)
                st.rerun()
            st.divider()

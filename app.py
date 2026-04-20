import streamlit as st
import os
import json

# --- FILE PATH CONFIGURATION ---
# This ensures the app finds the JSON file on the Streamlit server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "keys_database.json")

def load_keys():
    """Load keys from the JSON database file."""
    try:
        if not os.path.exists(DB_PATH):
            return {"keys": {}}
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Prevents the 'line 1 column 1' crash
        return {"keys": {}}

def main():
    st.set_page_config(page_title="RICOS SNIPER | AUTHENTICATION", layout="wide")
    
    # Corrected CSS section - fixed the 'unsafe_allow_html' error
    st.markdown("""
        <style>
        .main { background-color: #000000; color: white; }
        div.stButton > button { width: 100%; background-color: #111; border: 1px solid #333; color: white; }
        </style>
    """, unsafe_allow_html=True)

    # UI Layout based on your design
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("AUTHORIZATION")
        
        user_key = st.text_input("ENTER KEY", placeholder="RICOS-LT-XXXXXX")
        st.checkbox("Remember Me", value=True)
        
        if st.button("SIGN IN"):
            data = load_keys()
            allowed_keys = data.get("keys", {})
            
            # Checks against your actual keys
            if user_key in allowed_keys:
                st.success(f"Access Granted! Level: {allowed_keys[user_key]}")
            else:
                st.error("Invalid Key. Access Denied.")

    with col2:
        st.header("NEWS")
        st.info("RICOS SNIPER PANEL IS ONLINE")

if __name__ == "__main__":
    main()

import streamlit as st
import os
import json

# --- FILE PATH CONFIGURATION ---
# This ensures the app finds the JSON file regardless of where it's hosted
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
        # Handles errors seen in image_08b0e1.png and image_08c306.png
        return {"keys": {}}

def main():
    st.set_page_config(page_title="RICOS SNIPER | AUTHENTICATION", layout="wide")
    
    # Custom CSS to match your dark theme
    st.markdown("""
        <style>
        .main { background-color: #000000; color: white; }
        div.stButton > button { width: 100%; background-color: #111; border: 1px solid #333; color: white; }
        </style>
    """, unsafe_allow_index=True)

    # UI Layout based on image_08b0e1.png
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("AUTHORIZATION")
        
        user_key = st.text_input("ENTER KEY", placeholder="RICOS-LT-XXXXXX")
        remember_me = st.checkbox("Remember Me", value=True)
        
        if st.button("SIGN IN"):
            data = load_keys()
            allowed_keys = data.get("keys", {})
            
            # Check if key exists in your database
            if user_key in allowed_keys:
                st.success(f"Welcome! Access Level: {allowed_keys[user_key]}")
                # Add your main tool logic here
            else:
                st.error("Invalid Key. Please check your database.")

    with col2:
        st.header("NEWS")
        st.info("RICOS SNIPER PANEL IS ONLINE")

if __name__ == "__main__":
    main()

import streamlit as st
import os
import json
import secrets
import string
import pandas as pd
from datetime import datetime

# --- FILE PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "keys_database.json")

def load_data():
    """Load the full database."""
    try:
        if not os.path.exists(DB_PATH):
            return {"keys": {}, "owner_key": "RICOS-OWNER-ADMIN-999"}
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"keys": {}, "owner_key": "RICOS-OWNER-ADMIN-999"}

def save_data(data):
    """Save the updated database back to the JSON file."""
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

def generate_key():
    """Generates a secure key in the RICOS-LT-XXXX format."""
    suffix = ''.join(secrets.choice(string.get_encoding('ascii') + string.digits) for _ in range(12)).upper()
    return f"RICOS-LT-{suffix}"

def main():
    st.set_page_config(page_title="RICOS | KEY GENERATOR", layout="wide")

    # Ultra-Modern Cyberpunk UI
    st.markdown("""
        <style>
        .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
        .stButton > button { 
            background: linear-gradient(45deg, #0f0f0f, #1a1a1a);
            color: #00FF41; border: 1px solid #00FF41;
            border-radius: 2px; height: 3em; transition: 0.3s;
        }
        .stButton > button:hover { box-shadow: 0 0 15px #00FF41; color: white; }
        .key-card { 
            padding: 20px; border: 1px solid #333; background: #111; 
            border-radius: 10px; text-align: center; margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>SYSTEM AUTHENTICATION</h1>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 1, 1])
        with col:
            pin = st.text_input("MASTER ACCESS TOKEN", type="password")
            if st.button("BYPASS FIREWALL"):
                data = load_data()
                if pin == data.get("owner_key"):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
    else:
        # --- LOGGED IN: KEY GENERATOR PANEL ---
        st.title("📟 RICOS KEY COMMAND CENTER")
        
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("<div class='key-card'>", unsafe_allow_html=True)
            st.subheader("GENERATE NEW ACCESS")
            perm_level = st.selectbox("Permission Level", [1, 999, 9999])
            
            if st.button("GENERATE NEW KEY"):
                new_key = generate_key()
                data = load_data()
                data["keys"][new_key] = perm_level
                save_data(data)
                st.success(f"NEW KEY CREATED:\n{new_key}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.subheader("ACTIVE DATABASE")
            data = load_data()
            keys_dict = data.get("keys", {})
            
            if keys_dict:
                df = pd.DataFrame(list(keys_dict.items()), columns=["Key String", "Level"])
                # Displaying the keys in a clean, modern table
                st.dataframe(df, use_container_width=True)
                
                if st.button("CLEAR ALL KEYS (DANGER)"):
                    data["keys"] = {}
                    save_data(data)
                    st.rerun()
            else:
                st.info("No active keys found in database.")

        if st.sidebar.button("TERMINATE SESSION"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()

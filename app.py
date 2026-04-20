import streamlit as st
import os
import json
import pandas as pd

# --- FILE PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "keys_database.json")

def load_keys():
    """Load keys from the JSON database file."""
    try:
        if not os.path.exists(DB_PATH):
            return {}
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def main():
    st.set_page_config(page_title="RICOS SNIPER v2.0", layout="wide", initial_sidebar_state="collapsed")
    
    # Custom Modern Dark UI
    st.markdown("""
        <style>
        .main { background-color: #0d1117; color: #c9d1d9; }
        .stButton > button { 
            width: 100%; border-radius: 5px; border: 1px solid #30363d; 
            background-color: #21262d; color: #c9d1d9; font-weight: bold; 
        }
        .stButton > button:hover { border-color: #8b949e; background-color: #30363d; }
        .auth-header { text-align: center; color: #58a6ff; font-family: 'Courier New', monospace; letter-spacing: 3px; }
        div[data-testid="stMetricValue"] { color: #3fb950; }
        </style>
    """, unsafe_allow_html=True)

    # Authentication State
    if 'auth_level' not in st.session_state:
        st.session_state.auth_level = None

    if st.session_state.auth_level is None:
        # --- LOGIN SCREEN ---
        st.markdown("<h1 class='auth-header'>RICOS SNIPER SYSTEM</h1>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 2, 1])
        
        with col:
            with st.container():
                st.markdown("### AUTHORIZATION REQUIRED")
                user_key = st.text_input("ENTER ACCESS TOKEN", type="password", placeholder="RICOS-XXXX-XXXX")
                
                if st.button("INITIALIZE SESSION"):
                    data = load_keys()
                    allowed_keys = data.get("keys", {})
                    owner_key = data.get("owner_key")

                    if user_key == owner_key:
                        st.session_state.auth_level = "OWNER"
                        st.rerun()
                    elif user_key in allowed_keys:
                        st.session_state.auth_level = f"USER (Level {allowed_keys[user_key]})"
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED: INVALID TOKEN")
    else:
        # --- LOGGED IN DASHBOARD ---
        st.sidebar.title("RICOS NAV")
        st.sidebar.write(f"Status: **{st.session_state.auth_level}**")
        if st.sidebar.button("LOGOUT"):
            st.session_state.auth_level = None
            st.rerun()

        st.title("🎯 RICOS SNIPER PANEL")
        
        tab1, tab2 = st.tabs(["🚀 Sniper Console", "🔑 Key Management"])

        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Configuration")
                st.text_input("Contract Address", placeholder="0x...")
                st.number_input("Buy Amount (ETH/SOL)", min_value=0.01, value=0.1)
                if st.button("START SNIPER"):
                    st.warning("Sniper Engine Initializing... Standing by for liquidity.")
            
            with col_b:
                st.subheader("Network Status")
                st.metric("Ping", "24ms", "+2ms")
                st.metric("Gas Price", "15 Gwei", "-2 Gwei")

        with tab2:
            if st.session_state.auth_level == "OWNER":
                st.subheader("Database Overview")
                data = load_keys()
                
                # Show Owner Key
                st.info(f"**Current Owner Key:** `{data.get('owner_key')}`")
                
                # Table of all regular keys
                st.write("### Active User Keys")
                if "keys" in data:
                    df = pd.DataFrame(list(data["keys"].items()), columns=["Key ID", "Permission Level"])
                    st.table(df)
                else:
                    st.write("No user keys found.")
            else:
                st.error("You do not have permission to view the Key Database.")

if __name__ == "__main__":
    main()

import streamlit as st
import os
import json
import secrets
import string
import pandas as pd

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

def generate_key_string():
    """Generates a secure key string."""
    suffix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    return f"RICOS-LT-{suffix}"

def main():
    st.set_page_config(page_title="RICOS | ADMIN PANEL", layout="wide")

    # High-End Dark UI Theme
    st.markdown("""
        <style>
        .main { background-color: #080808; color: #ffffff; }
        .stTabs [data-baseweb="tab-list"] { gap: 24px; }
        .stTabs [data-baseweb="tab"] {
            height: 50px; background-color: #111; border-radius: 5px 5px 0 0;
            color: #58a6ff; font-weight: bold; padding: 0 20px;
        }
        .stTabs [aria-selected="true"] { background-color: #1f1f1f; border-bottom: 2px solid #58a6ff; }
        div[data-testid="stMetricValue"] { color: #58a6ff; font-family: monospace; }
        .key-box { 
            padding: 20px; border: 1px solid #30363d; background: #0d1117; 
            border-radius: 8px; margin-top: 20px; text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center; color: #58a6ff;'>RICOS TERMINAL</h1>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 1, 1])
        with col:
            pin = st.text_input("MASTER TOKEN", type="password")
            if st.button("LOGIN"):
                data = load_data()
                if pin == data.get("owner_key"):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("INVALID ACCESS TOKEN")
    else:
        st.title("📟 RICOS ADMIN DASHBOARD")
        
        tab1, tab2 = st.tabs(["⚡ KEY GENERATOR", "📂 KEY DATABASE"])

        with tab1:
            st.subheader("Create Subscription Token")
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                # Added the durations you requested
                duration = st.selectbox("Select Duration", ["1 Day", "1 Week", "1 Month", "Lifetime"])
                if st.button("CREATE KEY"):
                    new_key = generate_key_string()
                    data = load_data()
                    # Store duration as the value in the dictionary
                    data["keys"][new_key] = duration
                    save_data(data)
                    st.session_state.last_key = new_key
                    st.rerun()

            with col_b:
                if 'last_key' in st.session_state:
                    st.markdown(f"""
                        <div class="key-box">
                            <p style="color: #8b949e; margin-bottom: 5px;">SUCCESSFULLY GENERATED</p>
                            <h2 style="color: #3fb950; letter-spacing: 2px;">{st.session_state.last_key}</h2>
                        </div>
                    """, unsafe_allow_html=True)

        with tab2:
            st.subheader("Manage Active Access")
            data = load_data()
            keys_dict = data.get("keys", {})
            
            if keys_dict:
                # Convert the database into a clean table for the UI
                df = pd.DataFrame(list(keys_dict.items()), columns=["License Key", "Duration"])
                st.dataframe(df, use_container_width=True, height=400)
                
                col_c, col_d = st.columns([1, 4])
                with col_c:
                    if st.button("🗑️ WIPE ALL KEYS"):
                        data["keys"] = {}
                        save_data(data)
                        st.rerun()
            else:
                st.info("No active keys found in keys_database.json.")

        if st.sidebar.button("LOGOUT"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()

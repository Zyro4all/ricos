import streamlit as st
import random, string, json, requests, base64

# --- CONFIG ---
OWNER_KEY = "RICOS-OWNER-ADMIN-999"
REPO = "Zyro4all/ricos"
FILE_PATH = "keys_database.json"

# This pulls the token you'll put in Streamlit Advanced Settings
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("GitHub Token not found in Secrets!")
    st.stop()

st.set_page_config(page_title="RICOS ADMIN", page_icon="🎯")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ ADMIN LOGIN")
    pwd = st.text_input("Enter Admin Key", type="password")
    if st.button("Login"):
        if pwd == OWNER_KEY:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied")
else:
    st.title("🎯 KEY GENERATOR")
    tier = st.selectbox("Select Duration", ["1D", "1W", "1M", "LT"])
    
    if st.button("GENERATE & PUSH TO GITHUB"):
        new_key = f"RICOS-{tier}-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        days = {"1D": 1, "1W": 7, "1M": 30, "LT": 9999}[tier]

        url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            file_data = res.json()
            content = json.loads(base64.b64decode(file_data['content']).decode())
            content["keys"][new_key] = days
            encoded_content = base64.b64encode(json.dumps(content, indent=4).encode()).decode()
            
            update_payload = {"message": f"Add key {new_key}", "content": encoded_content, "sha": file_data['sha']}
            requests.put(url, headers=headers, json=update_payload)
            st.success(f"Key Live: {new_key}")
            st.code(new_key)
        else:
            st.error("GitHub Connection Failed")

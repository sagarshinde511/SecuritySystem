import streamlit as st
import requests
from ftplib import FTP
from urllib.parse import quote

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "SecuritySystem" 
BASE_WEB_URL = "https://aeprojecthub.in/SecuritySystem/" 

# DEFAULT LOGIN CREDENTIALS
DEFAULT_USER = "admin"
DEFAULT_PASS = "password123"
# -----------------------------------------------

st.set_page_config(page_title="Security Dashboard", layout="wide", page_icon="🛡️")

# --- LOGIN LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.sidebar.title("🔐 Access Control")
    user = st.sidebar.text_input("Username")
    pw = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if user == DEFAULT_USER and pw == DEFAULT_PASS:
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")

# If not logged in, show login screen and stop execution
if not st.session_state['logged_in']:
    st.title("🛡️ Security Cloud Gallery")
    st.info("Please login via the sidebar to access recordings.")
    login()
    st.stop() 

# --- MAIN DASHBOARD (Only visible if logged_in is True) ---

@st.cache_data(ttl=60)
def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_PATH)
        files = ftp.nlst()
        ftp.quit()
        valid = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        valid.sort(reverse=True)
        return valid
    except Exception as e:
        st.error(f"FTP Connection Error: {e}")
        return []

# Sidebar Logout
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

st.title("🛡️ Security Cloud Gallery")
st.markdown(f"**Welcome, {DEFAULT_USER}!**")
st.markdown("---")

videos = get_video_list()

if videos:
    selected_video = st.selectbox("Select a recording to view:", videos)
    video_url = f"{BASE_WEB_URL}{quote(selected_video)}"
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📺 Video Player")
        st.video(video_url)
        
    with col2:
        st.subheader("🛠️ Actions & Info")
        st.info(f"**File:** {selected_video}")
        
        try:
            with st.spinner('Fetching file for download...'):
                response = requests.get(video_url, timeout=15)
                if response.status_code == 200:
                    st.download_button(
                        label="📥 Download to Local",
                        data=response.content,
                        file_name=selected_video,
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    st.error("Download link broken (404/CORS)")
        except Exception as e:
            st.error("Could not prepare download.")
        
        st.markdown("---")
        st.markdown(f"[🔗 Open Direct Link]({video_url})")

else:
    st.warning("🔍 No videos found or FTP server unreachable.")
    if st.button("🔄 Refresh List"):
        st.cache_data.clear()
        st.rerun()

import streamlit as st
from ftplib import FTP
from urllib.parse import quote

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "SecuritySystem" 

# TRY CHANGING THIS TO HTTPS IF VIDEOS ARE BLOCKED
BASE_WEB_URL = "https://aeprojecthub.in/SecuritySystem/" 
# -----------------------------------------------

st.set_page_config(page_title="Security Dashboard", layout="wide")

@st.cache_data(ttl=60)
def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_PATH)
        files = ftp.nlst()
        ftp.quit()
        valid = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        valid.sort(reverse=True)
        return valid
    except Exception as e:
        st.error(f"FTP Error: {e}")
        return []

st.title("🛡️ Security Cloud Gallery")

videos = get_video_list()

if videos:
    selected = st.selectbox("Select Recording", videos)
    video_url = f"{BASE_WEB_URL}{quote(selected)}"
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Video Player")
        # Direct attempt
        st.video(video_url)
        
    with col2:
        st.subheader("Diagnostics")
        st.write(f"**File:** {selected}")
        st.markdown(f"[🔗 Test Direct Link]({video_url})")
        
        st.warning("""
        **If player is blank but 'Direct Link' works:** It is a CORS/HTTPS block. Add the .htaccess fix to your server.
        
        **If 'Direct Link' also fails to play:** The video is recorded in an unsupported codec (H.265/AVI). 
        Change camera settings to MP4 (H.264).
        """)
else:
    st.info("No videos found. Check FTP path and credentials.")

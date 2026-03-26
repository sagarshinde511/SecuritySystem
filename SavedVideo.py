import streamlit as st
from ftplib import FTP
from urllib.parse import quote

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "SecuritySystem" 
BASE_WEB_URL = "http://aeprojecthub.in/SecuritySystem/" 

# External Test Video (Known to work in all browsers)
EXTERNAL_TEST_URL = "https://www.w3schools.com/html/mov_bbb.mp4"
# -----------------------------------------------

st.set_page_config(page_title="SecuritySystem Gallery", layout="wide")

st.title("🛡️ SecuritySystem: Cloud Video Gallery")

# --- TEST MODE TOGGLE ---
test_mode = st.sidebar.toggle("Enable Test Video", value=False, help="Turn this on to check if the player works with an external source.")

@st.cache_data(ttl=300)
def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        try:
            ftp.cwd(REMOTE_PATH)
            files = ftp.nlst()
        finally:
            ftp.quit()
        
        valid_extensions = ('.mp4', '.avi', '.webm', '.mov')
        video_files = [f for f in files if f.lower().endswith(valid_extensions)]
        video_files.sort(reverse=True)
        return video_files
    except Exception as e:
        st.error(f"FTP Error: {e}")
        return []

# Sidebar
if st.sidebar.button("🔄 Refresh List"):
    st.cache_data.clear()
    st.rerun()

videos = get_video_list()

if not videos and not test_mode:
    st.info("No recordings found. Try enabling 'Test Video' in the sidebar.")
else:
    # Logic to decide which video to play
    if test_mode:
        selected_video = "EXTERNAL_TEST_VIDEO.mp4"
        video_url = EXTERNAL_TEST_URL
        st.sidebar.info("Currently playing external test video.")
    else:
        selected_video = st.selectbox("Select a recording:", videos)
        encoded_name = quote(selected_video)
        video_url = f"{BASE_WEB_URL}{encoded_name}"

    st.divider()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"🎥 Playing: {selected_video}")
        # The main player
        st.video(video_url)
        
    with col2:
        st.subheader("Controls")
        st.markdown(f"### [🔗 Direct Link]({video_url})")
        st.caption("If the video is black, click the link above. If the link works but the player doesn't, it's a CORS/SSL issue.")
        
    st.divider()
    
    # Grid Preview (Only shows if not in test mode)
    if not test_mode and videos:
        st.subheader("Recent Footage")
        cols = st.columns(3)
        for i, vid in enumerate(videos[:3]):
            with cols[i]:
                st.caption(vid)
                st.video(f"{BASE_WEB_URL}{quote(vid)}")

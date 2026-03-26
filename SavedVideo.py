import streamlit as st
from ftplib import FTP
from urllib.parse import quote
import os

# ---------------- CONFIGURATION ----------------
# Tip: If your Streamlit app is on HTTPS, your BASE_WEB_URL should also be HTTPS
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "SecuritySystem" 
BASE_WEB_URL = "http://aeprojecthub.in/SecuritySystem/" 
# -----------------------------------------------

st.set_page_config(page_title="SecuritySystem Video Gallery", layout="wide", page_icon="🛡️")

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stVideo { border: 2px solid #333; border-radius: 12px; }
    .video-card { padding: 10px; border: 1px solid #444; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SecuritySystem: Cloud Video Gallery")

@st.cache_data(ttl=300)
def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        try:
            ftp.cwd(REMOTE_PATH)
            files = ftp.nlst()
        except:
            st.error(f"Directory '{REMOTE_PATH}' not found on the server.")
            return []
        finally:
            ftp.quit()
        
        # Filter for common web-compatible formats
        valid_extensions = ('.mp4', '.avi', '.webm', '.mov')
        video_files = [f for f in files if f.lower().endswith(valid_extensions)]
        
        # Sort newest first (assumes filename starts with date/time)
        video_files.sort(reverse=True)
        return video_files
    except Exception as e:
        st.error(f"FTP Connection Error: {e}")
        return []

# Sidebar
st.sidebar.header("Navigation")
if st.sidebar.button("🔄 Refresh Gallery"):
    st.cache_data.clear()
    st.rerun()

videos = get_video_list()

if not videos:
    st.info("No security recordings found in the cloud folder.")
else:
    st.sidebar.success(f"Found {len(videos)} files")
    
    # 1. Main Player Section
    selected_video = st.selectbox("Select a recording to play:", videos)
    
    # URL Encoding handles spaces and special characters in filenames
    encoded_filename = quote(selected_video)
    video_url = f"{BASE_WEB_URL}{encoded_filename}"
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🎥 Currently Viewing: {selected_video}")
        
        # Format Warning
        if selected_video.lower().endswith('.avi'):
            st.warning("⚠️ .AVI files are not supported by most browsers. Convert to .MP4 (H.264) for direct playback.")
        
        # Streamlit Video Player
        # Note: If this is blank, check your browser console (F12) for 'Mixed Content' errors.
        st.video(video_url)

    with col2:
        st.subheader("Recording Options")
        st.write(f"**Filename:** `{selected_video}`")
        
        # Fallback Link (Crucial if the player fails)
        st.markdown(f"### [🔗 Open/Download Video]({video_url})")
        
        st.info("💡 **Troubleshooting:** If the video doesn't load, right-click the link above and select 'Save Link As' to view it locally.")

    st.divider()
    
    # 2. Recent Recordings Grid
    st.subheader("Recent Footage (Last 6)")
    grid_cols = st.columns(3)
    
    for i, vid in enumerate(videos[:6]):
        with grid_cols[i % 3]:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.caption(f"📅 {vid}")
            grid_video_url = f"{BASE_WEB_URL}{quote(vid)}"
            # Small preview player
            st.video(grid_video_url)
            st.markdown('</div>', unsafe_allow_html=True)

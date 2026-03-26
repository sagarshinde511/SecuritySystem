import streamlit as st
from ftplib import FTP
import pandas as pd
from urllib.parse import quote

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "SecuritySystem" 
BASE_WEB_URL = "http://aeprojecthub.in/SecuritySystem/"
# -----------------------------------------------

st.set_page_config(page_title="SecuritySystem Video Gallery", layout="wide", page_icon="🛡️")

# Custom CSS to improve the video player UI
st.markdown("""
    <style>
    .stVideo { margin-bottom: 20px; border-radius: 10px; }
    .video-card { border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SecuritySystem: Cloud Video Gallery")

@st.cache_data(ttl=300)  # Cache results for 5 minutes
def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        try:
            ftp.cwd(REMOTE_PATH)
        except:
            st.error(f"Directory '{REMOTE_PATH}' not found on server.")
            ftp.quit()
            return []

        # Get all filenames
        files = ftp.nlst()
        ftp.quit()
        
        # Filter for common video formats
        valid_extensions = ('.mp4', '.avi', '.mov', '.webm')
        video_files = [f for f in files if f.lower().endswith(valid_extensions)]
        
        # Sort by name (usually timestamped) newest first
        video_files.sort(reverse=True)
        return video_files
    except Exception as e:
        st.error(f"FTP Connection Error: {e}")
        return []

# Sidebar Controls
st.sidebar.header("Controls")
if st.sidebar.button("🔄 Refresh Gallery"):
    st.cache_data.clear()
    st.rerun()

videos = get_video_list()

if not videos:
    st.info("No security videos found in the remote folder.")
else:
    st.sidebar.success(f"Found {len(videos)} recordings")
    
    # 1. Main Player Section
    selected_video = st.selectbox("Select a recording to play:", videos)
    
    # URL Encode the filename (Crucial for filenames with spaces/dots)
    encoded_filename = quote(selected_video)
    video_url = f"{BASE_WEB_URL}{encoded_filename}"
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🎥 Playing: {selected_video}")
        
        # Logic for AVI vs MP4
        if selected_video.lower().endswith('.avi'):
            st.warning("⚠️ .AVI detected. This format usually requires downloading to view.")
            st.video(video_url) # Attempt play anyway
        else:
            st.video(video_url)

    with col2:
        st.subheader("Details & Download")
        st.info(f"**Filename:** {selected_video}")
        st.markdown(f"**Direct Link:** [Open in Browser]({video_url})")
        
        # Manual Download Button
        st.download_button(
            label="💾 Download Video File",
            data="",
            file_name=selected_video,
            help="Right

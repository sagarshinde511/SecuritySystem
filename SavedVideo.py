import streamlit as st
from ftplib import FTP
import pandas as pd

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "FireFighter"  # Updated folder name
BASE_WEB_URL = "http://aeprojecthub.in/SecuritySystem/" # Updated URL
# -----------------------------------------------

st.set_page_config(page_title="SecuritySystem Video Gallery", layout="wide")

st.title("🛡️ SecuritySystem: Cloud Video Gallery")
st.markdown(f"Accessing recordings from: `{BASE_WEB_URL}`")

def get_video_list():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        # Ensure we navigate to the correct directory
        try:
            ftp.cwd(REMOTE_PATH)
        except:
            st.error(f"Directory '{REMOTE_PATH}' not found on server.")
            return []

        # Get all filenames in the folder
        files = ftp.nlst()
        ftp.quit()
        
        # Updated Filter: Check for both .mp4 and .avi (case-insensitive)
        valid_extensions = ('.mp4', '.avi')
        video_files = [f for f in files if f.lower().endswith(valid_extensions)]
        
        # Sort by newest first (assuming naming convention includes date/time)
        video_files.sort(reverse=True)
        return video_files
    except Exception as e:
        st.error(f"Error connecting to FTP: {e}")
        return []

# Sidebar for controls
if st.sidebar.button("🔄 Refresh Gallery"):
    st.cache_data.clear()

videos = get_video_list()

if not videos:
    st.info("No security videos found in the folder.")
else:
    st.sidebar.write(f"Total Files Found: {len(videos)}")
    
    # Selection box to pick a video
    selected_video = st.selectbox("Select a recording to play:", videos)
    
    # Layout: Top video player
    st.subheader(f"Viewing: {selected_video}")
    video_url = BASE_WEB_URL + selected_video
    
    # Handling .avi browser limitations
    if selected_video.lower().endswith('.avi'):
        st.warning("⚠️ .AVI files may not play directly in all browsers. If it doesn't load, use the link below.")
        st.markdown(f"[Download or Open Video Link]({video_url})")
    
    st.video(video_url)
    
    st.divider()
    
    # Bottom Layout: Grid gallery
    st.subheader("Recent Recordings")
    cols = st.columns(3)
    for i, vid in enumerate(videos[:9]): # Show top 9 in grid
        with cols[i % 3]:
            st.caption(f"📄 {vid}")
            # Use st.video for previewing (works best for MP4)
            st.video(BASE_WEB_URL + vid)

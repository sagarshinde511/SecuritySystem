import streamlit as st
from ftplib import FTP
from urllib.parse import quote

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "SecuritySystem" 
BASE_WEB_URL = "https://aeprojecthub.in/SecuritySystem/"
# -----------------------------------------------

st.set_page_config(page_title="SecuritySystem Video Gallery", layout="wide", page_icon="🛡️")

# Custom CSS for styling
st.markdown("""
    <style>
    .video-container {
        border: 1px solid #444;
        border-radius: 10px;
        padding: 10px;
        background-color: #1e1e1e;
        margin-bottom: 20px;
    }
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
            st.error(f"Directory '{REMOTE_PATH}' not found.")
            return []
        finally:
            ftp.quit()
        
        # Filter and sort
        valid_exts = ('.mp4', '.avi', '.mov', '.webm')
        video_files = [f for f in files if f.lower().endswith(valid_exts)]
        video_files.sort(reverse=True)
        return video_files
    except Exception as e:
        st.error(f"FTP Error: {e}")
        return []

# Sidebar
st.sidebar.header("Navigation")
if st.sidebar.button("🔄 Refresh Gallery"):
    st.cache_data.clear()
    st.rerun()

videos = get_video_list()

if not videos:
    st.info("No recordings found in the cloud storage.")
else:
    st.sidebar.write(f"Total Recordings: {len(videos)}")
    
    # Selection
    selected_video = st.selectbox("Pick a recording to view:", videos)
    
    # URL Prep
    encoded_name = quote(selected_video)
    video_url = f"{BASE_WEB_URL}{encoded_name}"
    
    st.divider()

    # Main Viewing Area
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"🎥 Now Playing: {selected_video}")
        if selected_video.lower().endswith('.avi'):
            st.warning("⚠️ .AVI detected. If the player is blank, please use the download link in the right panel.")
        
        # Streamlit Player
        st.video(video_url)

    with col2:
        st.subheader("Video Info")
        st.write(f"**Name:** \n`{selected_video}`")
        
        st.markdown(f"### [🔗 Open Direct Link]({video_url})")
        
        # Fixed the string literal error here
        st.info("💡 Pro Tip: If the video won't play, right-click the link above and choose 'Save Link As' to download.")

    st.divider()
    
    # Recent Grid (Top 6)
    st.subheader("Recent Footage (Quick Preview)")
    grid_cols = st.columns(3)
    for index, vid_name in enumerate(videos[:6]):
        with grid_cols[index % 3]:
            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            st.caption(f"📄 {vid_name}")
            # Smaller player for grid
            st.video(f"{BASE_WEB_URL}{quote(vid_name)}")
            st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import requests
from ftplib import FTP
from urllib.parse import quote

# ---------------- CONFIGURATION ----------------
FTP_HOST = "82.180.143.66"
FTP_USER = "u263681140"
FTP_PASS = "SagarA@2025"
REMOTE_PATH = "SecuritySystem" 

# Base URL for playing and downloading videos via HTTP
BASE_WEB_URL = "https://aeprojecthub.in/SecuritySystem/" 
# -----------------------------------------------

st.set_page_config(page_title="Security Dashboard", layout="wide", page_icon="🛡️")

@st.cache_data(ttl=60)
def get_video_list():
    """Connects to FTP and retrieves a list of video files."""
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(REMOTE_PATH)
        files = ftp.nlst()
        ftp.quit()
        
        # Filter for common video formats
        valid = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        valid.sort(reverse=True)  # Newest files usually have higher timestamps/names
        return valid
    except Exception as e:
        st.error(f"FTP Connection Error: {e}")
        return []

st.title("🛡️ Security Cloud Gallery")
st.markdown("---")

# Initialize the video list to prevent NameError
videos = get_video_list()

if videos:
    # Sidebar or Top selection
    selected_video = st.selectbox("Select a recording to view:", videos)
    
    # Construct the full URL
    video_url = f"{BASE_WEB_URL}{quote(selected_video)}"
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📺 Video Player")
        # Streamlit's built-in player
        st.video(video_url)
        
    with col2:
        st.subheader("🛠️ Actions & Info")
        st.info(f"**File:** {selected_video}")
        
        # --- DOWNLOAD LOGIC ---
        try:
            # We fetch the video data so the user can download it locally
            with st.spinner('Preparing download...'):
                response = requests.get(video_url, timeout=10)
                if response.status_code == 200:
                    st.download_button(
                        label="📥 Download to Local",
                        data=response.content,
                        file_name=selected_video,
                        mime="video/mp4",
                        use_container_width=True
                    )
                else:
                    st.error("Could not fetch file for download.")
        except Exception as e:
            st.error(f"Download Error: {e}")
        
        st.markdown("---")
        st.markdown(f"[🔗 Open Direct Link]({video_url})")
        
        with st.expander("Help & Diagnostics"):
            st.write("""
            - **Black screen?** Check if your browser supports the codec (H.264 is best).
            - **File not found?** Ensure the filename on FTP matches the URL path.
            - **Slow loading?** Large files are being streamed from your host server.
            """)

else:
    st.warning("🔍 No videos found. Please check your FTP credentials or the REMOTE_PATH folder.")
    if st.button("🔄 Retry Connection"):
        st.cache_data.clear()
        st.rerun()

# Footer
st.markdown("---")
st.caption("Security System Dashboard © 2026")

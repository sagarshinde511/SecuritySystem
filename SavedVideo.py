import streamlit as st
import requests  # Added for downloading from the web URL
from ftplib import FTP
from urllib.parse import quote

# ... [Keep your existing CONFIGURATION and get_video_list() function] ...

if videos:
    selected = st.selectbox("Select Recording", videos)
    video_url = f"{BASE_WEB_URL}{quote(selected)}"
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Video Player")
        st.video(video_url)
        
    with col2:
        st.subheader("Actions & Info")
        st.write(f"**File:** {selected}")
        
        # --- NEW DOWNLOAD SECTION ---
        try:
            # We fetch the video data into memory to allow the browser to download it
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                st.download_button(
                    label="📥 Download Video",
                    data=response.content,
                    file_name=selected,
                    mime="video/mp4"
                )
            else:
                st.error("Could not fetch video for download.")
        except Exception as e:
            st.error(f"Download Error: {e}")
        # -----------------------------

        st.markdown(f"[🔗 Test Direct Link]({video_url})")
        
        st.warning("""
        **Troubleshooting:**
        - If the player is blank, check CORS settings.
        - If download fails, check server permissions.
        """)

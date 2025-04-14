import streamlit as st
import requests
import pycountry
from streamlit_lottie import st_lottie

# ------------------- Helper Functions -------------------

def get_language_name(code):
    """Convert language code to language name"""
    try:
        language = pycountry.languages.get(alpha_2=code)
        return language.name if language else code
    except:
        return code

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

def save_to_history(text, language, source):
    """Send extracted data to backend history"""
    payload = {
        "text": text,
        "language": language,
        "source": source
    }
    try:
        response = requests.post("http://localhost:8000/save_extraction", json=payload)
        if response.status_code == 200:
            st.success("✅ Content saved to history!")
        else:
            st.error("❌ Failed to save history.")
    except Exception as e:
        st.error(f"Error: {e}")

# ------------------- UI Initialization -------------------

# Load Lottie Animation
lottie_url = "https://assets5.lottiefiles.com/packages/lf20_1pxqjqps.json"
lottie_animation = load_lottie_url(lottie_url)

if lottie_animation:
    st_lottie(lottie_animation, speed=1, width=700, height=400, key="header_lottie")
else:
    st.warning("⚠️ Unable to load Lottie animation.")

# Title and Description
st.title("📊 Multimedia & Multilingual Information Extractor")
st.markdown("""
    This app lets you:
    - 🎙️ Transcribe audio and video files
    - 🖼️ Extract text from images
    - 📄 Read content from TXT and PDF files
    - 🌐 Detect languages automatically
    - 🗃️ Store and search past extractions
""")

# ------------------- Sidebar Navigation -------------------

option = st.sidebar.selectbox("Choose an Option", ["Upload Media", "View History"])

# ------------------- Media Upload Page -------------------

def upload_media():
    st.subheader("📤 Upload Your Media File")

    media_file = st.file_uploader(
        "Choose a file (Audio, Video, Image, TXT, or PDF)",
        type=["mp3", "mp4", "jpg", "jpeg", "png", "txt", "pdf"]
    )

    if media_file:
        st.write(f"**Uploaded:** `{media_file.name}`")
        file_type = media_file.type

        # Preview based on media type
        if 'audio' in file_type:
            st.audio(media_file)
            process_audio(media_file)

        elif 'video' in file_type:
            st.video(media_file)
            process_video(media_file)

        elif 'image' in file_type:
            st.image(media_file)
            process_image(media_file)

        elif 'text/plain' in file_type:
            process_txt(media_file)

        elif 'application/pdf' in file_type:
            process_pdf(media_file)

# ------------------- Processing Functions -------------------

def process_audio(media_file):
    st.info("⏳ Transcribing audio...")
    try:
        response = requests.post("http://localhost:8000/upload/audio", files={"file": media_file})
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Transcription complete!")
            st.markdown(f"**Language:** {get_language_name(result['language'])}")
            st.code(result["text"])
            save_to_history(result["text"], result["language"], "audio")
        else:
            st.error("❌ Failed to process audio.")
    except Exception as e:
        st.error(f"Error: {e}")

def process_video(media_file):
    st.info("⏳ Transcribing video...")
    try:
        response = requests.post("http://localhost:8000/upload/video", files={"file": media_file})
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Transcription complete!")
            st.markdown(f"**Language:** {get_language_name(result['language'])}")
            st.code(result["text"])
            save_to_history(result["text"], result["language"], "video")
        else:
            st.error("❌ Failed to process video.")
    except Exception as e:
        st.error(f"Error: {e}")

def process_image(media_file):
    st.info("⏳ Extracting text from image...")
    try:
        response = requests.post("http://localhost:8000/upload/image", files={"file": media_file})
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Text extracted!")
            st.markdown(f"**Language:** {get_language_name(result['language'])}")
            st.code(result["text"])
            save_to_history(result["text"], result["language"], "image")
        else:
            st.error("❌ Failed to process image.")
    except Exception as e:
        st.error(f"Error: {e}")

def process_txt(media_file):
    st.info("⏳ Processing TXT file...")
    try:
        response = requests.post("http://localhost:8000/upload/txt", files={"file": media_file})
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Text extracted from TXT!")
            st.markdown(f"**Language:** {get_language_name(result['language'])}")
            st.code(result["text"])
            save_to_history(result["text"], result["language"], "txt")
        else:
            st.error("❌ Failed to process TXT.")
    except Exception as e:
        st.error(f"Error: {e}")

def process_pdf(media_file):
    st.info("⏳ Processing PDF file...")
    try:
        response = requests.post("http://localhost:8000/upload/pdf", files={"file": media_file})
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Text extracted from PDF!")
            st.markdown(f"**Language:** {get_language_name(result['language'])}")
            st.code(result["text"])
            save_to_history(result["text"], result["language"], "pdf")
        else:
            st.error("❌ Failed to process PDF.")
    except Exception as e:
        st.error(f"Error: {e}")

# ------------------- History Page -------------------

def view_history():
    st.subheader("🔍 Extraction History")

    lang_filter = st.text_input("Filter by Language Code (e.g., en, fr, hi)")
    source_filter = st.selectbox("Filter by Source Type", ["", "audio", "image", "video", "txt", "pdf"])

    params = {}
    if lang_filter:
        params["language"] = lang_filter
    if source_filter:
        params["source"] = source_filter

    try:
        response = requests.get("http://localhost:8000/history", params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                st.info("No results found.")
            for item in data:
                st.markdown(f"📁 **Source**: `{item['source']}`")
                st.markdown(f"🌐 **Language**: {get_language_name(item['language'])}")
                st.markdown(f"🕒 **Timestamp**: `{item['timestamp']}`")
                st.markdown(f"📝 **Extracted Text:**")
                st.code(item["text"])
                st.markdown("---")
        else:
            st.error("❌ Failed to fetch history.")
    except Exception as e:
        st.error(f"Error: {e}")

# ------------------- Main -------------------

if option == "Upload Media":
    upload_media()
elif option == "View History":
    view_history()
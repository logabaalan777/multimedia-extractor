# 📊 Multimedia & Multilingual Information Extractor

A powerful application built with **Streamlit** (Frontend) and **FastAPI** (Backend) to extract and analyze content from various media types including audio, video, image, text, and PDF. It automatically detects the language 🌐 and stores a history of all extractions 📜.

---

## ✨ Features

- 🎙️ **Audio & Video**: Extract speech as text using whisper
- 🖼️ **Images**: Extract text using OCR (Tesseract)
- 📄 **Text & PDF**: Read and process content directly
- 🌐 **Language Detection**: Auto-detects language (English, Tamil, Hindi, etc.)
- 💾 **History Storage**: Maintains logs with timestamps
- ⚡ **FastAPI Backend**: Modular, fast API endpoints
- 🧠 **Streamlit UI**: Clean and interactive frontend

---

## 🚀 Getting Started

### 🔧 1. Clone the Repository

# Multimedia Extractor 🎯

A powerful tool to extract text from various media formats including images, audio, video, and documents.

![Multimedia Extractor](https://img.shields.io/badge/Multimedia-Extractor-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- Extract text from images using OCR technology
- Transcribe speech from audio files
- Extract text content from video files
- Parse and extract text from documents (PDF, TXT)
- Automatic language detection for extracted content
- Search functionality through extracted content
- Multilingual support
- User-friendly web interface

## 🚀 Quick Start

### 📦 1. Clone the Repository

```bash
git clone https://github.com/logabaalan777/multimedia-extractor.git
cd multimedia-extractor
```

### 📦 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🚀 3. Run the Application

#### ▶️ Start FastAPI Server (Backend)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 💻 Start Streamlit App (Frontend)

```bash
streamlit run app.py
```

## 📁 Project Structure

```
.
├── app.py                 # Streamlit frontend
├── main.py                # FastAPI backend
├── models/                # Pydantic models
├── services/              # Image, audio, video processing logic
├── utils/                 # Helper functions (language detection, saving history)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🧪 Supported File Types

| Media Type | Supported Formats |
|------------|-------------------|
| Audio      | .mp3              |
| Video      | .mp4              |
| Image      | .jpg, .jpeg, .png |
| Document   | .txt, .pdf        |

## 🧰 Tech Stack

- Python 3.9+
- FastAPI - backend APIs
- Streamlit - frontend UI
- Pydantic - data validation
- Tesseract OCR - text from image
- LangDetect / pycountry - language detection
- MongoDB (Optional) - to store history and allow search

## 💡 Usage Examples

### 1. Extract Text from an Image

1. Navigate to the Image tab
2. Upload an image file
3. Click "Extract Text"
4. View the extracted text with detected language

### 2. Transcribe Audio

1. Navigate to the Audio tab
2. Upload an audio file
3. Click "Transcribe"
4. View the transcription with detected language

### 3. Extract Text from Video

1. Navigate to the Video tab
2. Upload a video file
3. Click "Extract"
4. View the extracted text content

### 4. Parse Documents

1. Navigate to the Documents tab
2. Upload a PDF or TXT file
3. Click "Extract Text"
4. View the extracted content

## 🛠️ Development Roadmap

- [x] Project setup and structure
- [ ] Extract text from image (OCR)
- [ ] Extract text from audio (Whisper)
- [ ] Extract text from video
- [ ] Extract text from TXT and PDF
- [ ] Language detection
- [ ] Search extracted data using MongoDB
- [ ] Multilingual UI support (Tamil, Hindi, etc.)

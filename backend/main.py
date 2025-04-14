from fastapi import FastAPI, File, UploadFile, HTTPException
from utils.audio_processing import transcribe_audio
from utils.image_processing import extract_text_from_image
from utils.video_processing import extract_text_from_video
from database import insert_data
from models import ExtractedTextResponse
from datetime import datetime
from langdetect import detect
from fastapi import Query
from fastapi.responses import JSONResponse
from typing import List
from database import get_all_data
from PyPDF2 import PdfReader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_size: int):
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request: Request, call_next):
        if request.headers.get('content-length'):
            content_length = int(request.headers['content-length'])
            if content_length > self.max_size:
                return JSONResponse(
                    {"detail": f"Request body exceeds the size limit of {self.max_size} bytes."},
                    status_code=400
                )
        response = await call_next(request)
        return response

app = FastAPI()

app.add_middleware(
    GZipMiddleware 
)

app.add_middleware(
    LimitRequestSizeMiddleware,
    max_size=100 * 1024 * 1024 
)

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"
    
@app.post("/save_extraction")
async def save_extraction(payload: dict):
    try:
        text = payload.get("text")
        language = payload.get("language")
        source = payload.get("source")

        insert_data(source, text, language)
        
        return JSONResponse(content={"message": "Content saved to history!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)
    
@app.get("/history", response_model=List[ExtractedTextResponse])
async def get_history(language: str = Query(None), source: str = Query(None)):
    data = get_all_data(language=language, source=source)
    return data

@app.post("/upload/audio", response_model=ExtractedTextResponse)
async def upload_audio(file: UploadFile = File(...)):
    text = await transcribe_audio(file)
    lang = detect_language(text)
    insert_data("audio", text, lang)
    return ExtractedTextResponse(source="audio", text=text, language=lang, timestamp=str(datetime.now()))

@app.post("/upload/txt", response_model=ExtractedTextResponse)
async def upload_txt(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    lang = detect_language(text)
    insert_data("txt", text, lang)
    return ExtractedTextResponse(source="txt", text=text, language=lang, timestamp=str(datetime.now()))

@app.post("/upload/pdf", response_model=ExtractedTextResponse)
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.pdf", "wb") as f:
        f.write(contents)

    reader = PdfReader("temp.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    lang = detect_language(text)
    insert_data("pdf", text, lang)
    return ExtractedTextResponse(source="pdf", text=text, language=lang, timestamp=str(datetime.now()))

@app.post("/upload/image", response_model=ExtractedTextResponse)
async def upload_image(file: UploadFile = File(...)):
    text = await extract_text_from_image(file)
    lang = detect_language(text)
    insert_data("image", text, lang)
    return ExtractedTextResponse(source="image", text={"content": text["text"]}, language=text["language"], timestamp=str(datetime.now()))

@app.post("/upload/video", response_model=ExtractedTextResponse)
async def upload_video(file: UploadFile = File(...)):
    text = await extract_text_from_video(file)
    lang = detect_language(text)
    insert_data("video", text, lang)
    return ExtractedTextResponse(source="video", text=text, language=lang, timestamp=str(datetime.now()))
import whisper
import tempfile
import os
from datetime import datetime

model = whisper.load_model("medium")

async def transcribe_audio(file):
    os.environ["PATH"] += os.pathsep + r"C:\Users\LOGABAALAN\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        content = await file.read()
        temp.write(content)
        temp.flush()

        result = model.transcribe(temp.name)

        return result["text"]
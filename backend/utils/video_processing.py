from moviepy.editor import VideoFileClip
import whisper
import tempfile
import os

model = whisper.load_model("small")

async def extract_text_from_video(file):
    os.environ["PATH"] += os.pathsep + r"C:\Users\LOGABAALAN\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin"
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
            content = await file.read()
            temp.write(content)
            temp.flush()

            video = VideoFileClip(temp.name)
            audio_path = temp.name.replace(".mp4", ".mp3")
            video.audio.write_audiofile(audio_path)

            audio_length = video.audio.duration  
            chunk_duration = 30  
            num_chunks = int(audio_length // chunk_duration) + 1

            transcriptions = []
            
            for i in range(num_chunks):
                start_time = i * chunk_duration
                end_time = min((i + 1) * chunk_duration, audio_length)

                chunk_audio_path = audio_path.replace(".mp3", f"_chunk_{i}.mp3")
                video.audio.subclip(start_time, end_time).write_audiofile(chunk_audio_path)

                result = model.transcribe(chunk_audio_path)
                if 'text' in result:
                    transcriptions.append(result["text"])

            final_transcription = " ".join(transcriptions)
            print(final_transcription)
            return final_transcription
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


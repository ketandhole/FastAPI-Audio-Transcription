from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
import os
import shutil
import logging
import subprocess
from whisper_models import transcribe_audio
from summarizer import summarize_text

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logging.info(f"File uploaded successfully: {file_path}")
        return JSONResponse(content={"filename": file.filename, "detail": "File uploaded successfully"})
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/transcribe/")
async def transcribe_endpoint():
    try:
        file_path = r"C:\Users\Admin\Desktop\Audio\uploads\sample1.mp3"
        
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")

        ffmpeg_path = r'C:\ffmpeg\ffmpeg.exe'
        try:
            result = subprocess.run([ffmpeg_path, "-version"], check=True, capture_output=True, text=True)
            logging.info(f"FFmpeg is available: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg error: {e.stderr}")
            raise HTTPException(status_code=500, detail="FFmpeg is not available")
        except FileNotFoundError:
            logging.error("FFmpeg executable not found")
            raise HTTPException(status_code=500, detail="FFmpeg executable not found")

        # Transcribe the audio file
        transcription, timestamps = transcribe_audio(file_path)
        
        if transcription:
            return {"transcription": transcription, "timestamps": timestamps}
        else:
            raise HTTPException(status_code=500, detail="Transcription failed.")
    except HTTPException as e:
        raise e 
    except Exception as e:
        logging.error(f"Error in transcription endpoint: {e}")
        raise HTTPException(status_code=500, detail="Transcription endpoint error.")

@app.post("/summarize/")
async def summarize_endpoint(text: str):
    try:
        summary = summarize_text(text)
        return {"summary": summary}
    except Exception as e:
        logging.error(f"Error in summarization endpoint: {e}")
        raise HTTPException(status_code=500, detail="Summarization endpoint error.")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

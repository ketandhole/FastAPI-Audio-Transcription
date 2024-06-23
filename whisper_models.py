import whisper
import logging
import os

def transcribe_audio(file_path: str):
    try:
        if not os.path.exists(file_path):
            logging.error(f"File does not exist: {file_path}")
            return None, None

        logging.info(f"Starting transcription for: {file_path}")
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        logging.info(f"Transcription result: {result}")
        transcription = result['text']
        timestamps = result['segments']
        return transcription, timestamps
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        return None, None

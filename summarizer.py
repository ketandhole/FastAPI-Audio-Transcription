
from transformers import pipeline

model_name = "sshleifer/distilbart-cnn-12-6"
revision = "a4f8f3e"

summarizer = pipeline("summarization", model=model_name, revision=revision)

def summarize_text(text: str):
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

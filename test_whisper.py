# Save as test_whisper.py
from transformers import pipeline

asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    chunk_length_s=2,
    device=-1
)
print("Whisper loaded!")
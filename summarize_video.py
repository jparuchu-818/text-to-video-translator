import os
import tempfile
import whisper
from deep_translator import GoogleTranslator
import requests
from moviepy.editor import VideoFileClip

#extracts audio from a video file and saves it as a .wav file
def extract_audio(video_path: str, audio_path: str):
    print("[INFO] Extracting audio from video...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    print("[✔] Audio saved to:", audio_path)

#uses whisper to transcribe the audio
def transcribe_audio(audio_path: str) -> str:
    print("[INFO] Transcribing Hindi audio using Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language='hi')
    print("[✔] Transcription complete.")
    return result["text"]

#google translator for hindi/any other languae to english
def translate_to_english(hindi_text: str) -> str:
    print("[INFO] Translating Hindi transcription to English...")
    english_text = GoogleTranslator(source='hi', target='en').translate(hindi_text)
    print("[✔] Translation done.")
    return english_text

def summarize_text(text: str) -> str:
    print("[INFO] Generating summary using LLaMA 3 (local)...")
    prompt = f"Summarize the following into 3-4 lines:\n\n{text}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return response.json()['response'].strip()
    else:
        raise Exception(f"Failed to summarize: {response.text}")

def main():
    video_path = "final_output.mp4"

    if not os.path.exists(video_path):
        print(f"[ERROR] Video file not found: {video_path}")
        return

    with tempfile.TemporaryDirectory() as tempdir:
        audio_path = os.path.join(tempdir, "audio.wav")

        extract_audio(video_path, audio_path)

        hindi_transcription = transcribe_audio(audio_path)
        english_text = translate_to_english(hindi_transcription)
        summary = summarize_text(english_text)

        print("\n FINAL SUMMARY:")
        print("--------------------------------------------------")
        print(summary)
        print("--------------------------------------------------")

if __name__ == "__main__":
    main()

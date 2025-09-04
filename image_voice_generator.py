import os
from PIL import Image
from gtts import gTTS
from moviepy.editor import TextClip
from diffusers import StableDiffusionPipeline
import torch
from transformers import AutoTokenizer, AutoModel
from pydub import AudioSegment

#uses gpu if available, else CPU(very slow)
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_images_and_audio(text_en: str, text_hi: str, scene_number: int, voice_gender: str, output_dir: str):
    """
    Generates:
    - image from English text
    - Hindi audio from Hindi text
    - English subtitle .srt file
    Returns dict with file paths
    """

    print("[INFO] Generating image...")
    image = pipe(text_en).images[0]
    image_path = os.path.join(output_dir, f"scene_{scene_number:02d}.png")
    image.save(image_path)

    print("[INFO] Generating audio...") #uses gtts(female voice only)
    tts = gTTS(text=text_hi, lang='hi', slow=False)
    audio_path = os.path.join(output_dir, f"scene_{scene_number:02d}.mp3")
    tts.save(audio_path)

    print("[INFO] Generating subtitles...") # creates .srt file for storing subtitles per each scene
    subtitle_path = os.path.join(output_dir, f"scene_{scene_number:02d}.srt")
    with open(subtitle_path, "w", encoding="utf-8") as f:
        f.write("1\n")
        f.write("00:00:00,000 --> 00:00:05,000\n")
        f.write(text_en + "\n")

    return {
        "image": image_path,
        "audio": audio_path,
        "subtitle": subtitle_path
    }

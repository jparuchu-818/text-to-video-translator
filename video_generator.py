import os
import nltk
from deep_translator import GoogleTranslator
from grammar_utils import correct_grammar
from image_voice_generator import generate_images_and_audio
from video_composer import create_final_video
from nltk.tokenize import sent_tokenize

#sentenxe tokenizer(for scene spltting in videos)
nltk.download('punkt')  

def translate_to_hindi(text):
    return GoogleTranslator(source='en', target='hi').translate(text)

#2 senteces per scene default
def split_into_scenes(text, sentences_per_scene=2):
    sentences = sent_tokenize(text)
    scenes = []
    for i in range(0, len(sentences), sentences_per_scene):
        scene_text = " ".join(sentences[i:i + sentences_per_scene])
        scenes.append(scene_text)
    return scenes

def main():
    print("\n🎬 Text-to-Video Generator (Hindi Voice, English Subtitles)")
    print("-------------------------------------------------------------")
    
    input_text = input("Enter the English prompt to convert into video:\n> ")

    print("\n[1] Correcting grammar...")
    corrected_text = correct_grammar(input_text)
    print(f"[✔] Corrected: {corrected_text}")

    print("\n[2] Translating entire text to Hindi for voiceover...")
    full_hindi = translate_to_hindi(corrected_text)
    print(f"[✔] Hindi Translation: {full_hindi}")

    print("\n[3] Choose voice type: male / female")
    voice_gender = input("Voice: ").strip().lower()
    if voice_gender not in ['male', 'female']:
        print("[!] Invalid input. Defaulting to 'female'.")
        voice_gender = 'female'

    print("\n[4] Splitting content into scenes...")
    scenes_en = split_into_scenes(corrected_text)
    print(f"[✔] Total Scenes: {len(scenes_en)}")

    # Output folder
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    scene_files = []
    for i, scene_en in enumerate(scenes_en):
        print(f"\n--- Generating Scene {i + 1} ---")
        scene_hi = translate_to_hindi(scene_en)
        data = generate_images_and_audio(
            text_en=scene_en,
            text_hi=scene_hi,
            scene_number=i + 1,
            voice_gender=voice_gender,
            output_dir=output_dir
        )
        scene_files.append(data)

    print("\n[5] Composing final video...")
    create_final_video(scene_files, output_path="final_output.mp4")
    print("\n Video successfully generated: final_output.mp4")


if __name__ == "__main__":
    main()

# 🎬 Text-to-Video Generator

This project is an AI-powered **Text-to-Video Generation Pipeline** that transforms plain text into engaging short videos with **images, voiceovers, and cinematic effects**.  

It combines the power of **local AI models** for text-to-image, speech synthesis, and video composition — so you can generate videos completely offline.

---

## 🚀 Features
- 📝 **Text Input** → Enter or load a script/story.
- 🖼 **Image Generation** → Uses Stable Diffusion to create scene visuals.
- 🎙 **Voice Narration** → Converts text to natural speech (Hindi/English supported).
- 🎥 **Video Composition** → Combines images + voiceover with cinematic effects (zoom, pan, fade).
- 💬 **Subtitles** → Auto-generated captions in English.
- 🌐 **Offline Support** → Works without internet once models are downloaded.

---

## 🛠 Tech Stack
- **Python 3.12+**
- [Stable Diffusion (Diffusers)](https://huggingface.co/docs/diffusers)
- [MoviePy](https://zulko.github.io/moviepy/)
- [gTTS / Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech
- [Ollama](https://ollama.ai) for grammar/translation assistance
- Supporting libraries: `torch`, `transformers`, `pydub`, `sentence-transformers`

---

## 📂 Project Structure
video-text/
│── assets/ # Generated images/audio
│── outputs/ # Final composed videos
│── image_voice_generator.py
│── video_composer.py
│── requirements.txt
│── README.md

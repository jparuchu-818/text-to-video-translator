from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, TextClip
import os


def create_final_video(scene_files: list, output_path: str = "final_output.mp4"):
    """
    Given a list of scene file dicts (image, audio, subtitle), compose a cinematic video.
    Adds fade-in/out, zoom effect, and overlays English subtitles.
    """
    print("[INFO] Creating final video...")

    clips = []

    for idx, scene in enumerate(scene_files):
        print(f"[INFO] Processing Scene {idx + 1}")

        #extract file paths
        image_path = scene['image']
        audio_path = scene['audio']
        subtitle_path = scene['subtitle']

        #this is to load audio for duration
        audio = AudioFileClip(audio_path)
        duration = audio.duration

        image = ImageClip(image_path).set_duration(duration) #match with audio duration after loading the image

        zoomed = image.resize(lambda t: 1 + 0.02 * t).set_position('center') #"Ken Burns style" for smooth zoom-in effect

        with open(subtitle_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) >= 3:
                subtitle_text = lines[2].strip()
            else:
                subtitle_text = ""

        subtitle = TextClip(
            subtitle_text,
            fontsize=40,
            font='Arial-Bold',
            color='white',
            stroke_color='black',
            stroke_width=2,
            method='caption',
            size=(zoomed.w * 0.8, None)
        ).set_position(("center", "bottom")).set_duration(duration)

        final = CompositeVideoClip([zoomed, subtitle])
        final = final.set_audio(audio)
        clips.append(final.fadein(0.5).fadeout(0.5))

    full_video = concatenate_videoclips(clips, method="compose")
    full_video.write_videofile(output_path, fps=24)

    print(f"[] Final video saved to: {output_path}")

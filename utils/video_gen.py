import os
import time
import traceback

# SET IMAGEMAGICK PATH BEFORE ANY MOVIEPY IMPORTS
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip

def generate_video(summary, keywords):
    """
    Generates a summary video using MoviePy with text slides.
    """
    if not summary:
        print("CRITICAL: No summary provided for video generation.")
        return None
    
    # Check for latest audio file
    try:
        audio_files = [f for f in os.listdir("static/audio") if f.endswith(".mp3")]
        if not audio_files:
            print("CRITICAL: No audio files found in static/audio")
            return None
        
        latest_audio = sorted(audio_files)[-1]
        audio_path = os.path.join("static/audio", latest_audio)
    except Exception as e:
        print(f"CRITICAL: Error accessing audio files: {e}")
        return None
    
    filename = f"video_{int(time.time())}.mp4"
    output_path = os.path.join("static/video", filename)
    
    try:
        print(f"DEBUG: Processing video with audio: {audio_path}")
        audio = AudioFileClip(audio_path)
        
        # Cap duration for efficiency
        duration = min(audio.duration, 60) 
        audio = audio.subclip(0, duration)
        
        # Color palette
        bg_hex = "#1a0b14" # Dark background
        accent_hex = "#b90e6c" # Magenta accent
        
        if keywords and any(kw.lower() in ['math', 'physics', 'science', 'tech', 'ai'] for kw in keywords):
            bg_hex = "#0a1a24" # Dark blue
            accent_hex = "#00f2ff" # Cyan
            
        background = ColorClip(size=(1280, 720), color=[int(bg_hex[i:i+2], 16) for i in (1, 3, 5)]).set_duration(duration)
        
        # Improved slide splitting: split by sentence or semi-colon
        import re
        points = re.split(r'[.;\n]+', summary)
        points = [p.strip() for p in points if len(p.strip()) > 15]
        
        # Fallback if splitting fails
        if not points:
            points = [summary[i:i+150] for i in range(0, len(summary), 150)][:5]
            
        print(f"DEBUG: Generated {len(points)} slides.")
        slide_duration = duration / len(points)
        clips = [background]
        
        # Title Overlay (persistent)
        try:
            header_bar = ColorClip(size=(1280, 80), color=[int(accent_hex[i:i+2], 16) for i in (1, 3, 5)]).set_duration(duration).set_opacity(0.8)
            clips.append(header_bar.set_position(('center', 0)))
            
            title_txt = TextClip("LEARNING SUMMARY", fontsize=40, color='white', font='Arial-Bold').set_duration(duration)
            clips.append(title_txt.set_position(('center', 20)))
        except Exception as e:
            print(f"WARNING: Title overlay failed: {e}")

        for i, point in enumerate(points):
            start_t = i * slide_duration
            
            try:
                # Slide text content
                txt = TextClip(
                    point,
                    fontsize=50,
                    color='white',
                    font='Arial',
                    size=(1100, 500),
                    method='caption',
                    align='center'
                ).set_start(start_t).set_duration(slide_duration).set_position('center')
                
                # Fade in/out
                txt = txt.crossfadein(0.5).crossfadeout(0.5)
                
                # Slide counter
                counter = TextClip(f"Slide {i+1} / {len(points)}", fontsize=24, color='white').set_start(start_t).set_duration(slide_duration)
                
                clips.append(txt)
                clips.append(counter.set_position((1100, 680)))
            except Exception as slide_err:
                print(f"ERROR: Failed to create slide {i}: {slide_err}")

        final_video = CompositeVideoClip(clips).set_duration(duration).set_audio(audio)
        
        print(f"DEBUG: Writing video file to {output_path}...")
        final_video.write_videofile(output_path, fps=12, codec='libx264', audio_codec='aac', bitrate="1500k", logger=None)
        
        print(f"DEBUG: Video generation successful: {filename}")
        return filename
    except Exception as e:
        print(f"CRITICAL: Video generation crashed: {e}")
        traceback.print_exc()
        return None

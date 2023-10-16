import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from gtts import gTTS
import shutil
import openai
from deep_translator import GoogleTranslator


openai.api_key = "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"
st.title("Video Translation App")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Upload the video
uploaded_video = st.file_uploader("Upload a video", type=["mp4"])
if uploaded_video:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_video.read())

if st.button("Translate Video"):
    st.write("Translating the video...")
    output_video_path='output_video.mp4'
    video_path = 'input.mp4'

    video = VideoFileClip(video_path)

    audio = video.audio

    audio.write_audiofile('output_audio.wav')

    video = video.set_audio(None)

    # Save the video without audio
    video.write_videofile(output_video_path, codec='libx264', audio_codec='aac', threads=4)
    video.close()
    audio.close()

    openai.api_key = "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"
    audio_file = "output_audio.wav" 
    audio_file= open(audio_file, "rb")
    text = openai.Audio.transcribe("whisper-1", audio_file)
    st.write(text)

    
    translated = GoogleTranslator(source='auto', target='hi').translate(text.text)
    st.write(translated)

    myobj = gTTS(text=translated, lang='hi' , slow=False)
    myobj.save("translated_audio.mp3")


    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
    import shutil

    # Paths to your input video, translated audio, and output video
    input_video_path = "input.mp4"
    translated_audio_path = "translated_audio.mp3"
    output_video_path = "final_video.mp4"

    # Load the input video and translated audio
    video_clip = VideoFileClip(input_video_path)
    audio_clip = AudioFileClip(translated_audio_path)

    # Ensure audio duration matches video duration
    if audio_clip.duration > video_clip.duration:
        # Trim the audio if it's longer than the video
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    elif audio_clip.duration < video_clip.duration:
        # Extend the audio by looping if it's shorter than the video
        num_loops = int(video_clip.duration / audio_clip.duration)
        audio_clip = audio_clip.volumex(num_loops)

    # Set the audio of the video to the translated audio
    video_clip = video_clip.set_audio(audio_clip)

    # Write the final video
    video_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac', threads=4)

    # Clean up intermediate files (optional)
    shutil.copy(translated_audio_path, "translated_audio_original.mp3")
    shutil.move("translated_audio_original.mp3", translated_audio_path)

    st.write("Translated audio appended to the video.")
    st.balloons()

    st.video(output_video_path)

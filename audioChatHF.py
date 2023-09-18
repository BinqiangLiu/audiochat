#audio recorder function: https://pypi.org/project/audio-recorder-streamlit/
#python -m pip install --upgrade pip; pip install -r requirements.txt
#python version: 3.10.11
#使用Audio record streamlit（https://pypi.org/project/audio-recorder-streamlit/）（https://github.com/Joooohan/audio-recorder-streamlit）录音
#使用SpeechRecognition 3.10.0（https://pypi.org/project/SpeechRecognition/）将录音转文字


import streamlit as st
import subprocess
import openai
import numpy as np
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import numpy as np
import ffmpeg
from langdetect import detect
from gtts import gTTS

# Load environment variables
from dotenv import load_dotenv
import os

st.set_page_config(
    page_title="语音AI随身聊 - 您的随身智能语音助手",
    page_icon=":rocket:",  # You can use Emoji as the page icon
    layout="centered",  # You can set the layout to "wide" or "centered"
)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are a helpful assistant."}]

st.title("语音AI随身聊")
st.write("---")
st.header("请用语音向AI智能助手提问！")
st.write("点击下方按钮输入语音（5秒无输入则自动停止）")
audio = audio_recorder(text="红色图标录音中，黑色停止", pause_threshold=5)
st.write("---")

try:
    if len(audio) > 0:
        # To play audio in frontend:
        st.write("↓↓↓播放您输入的语音！")
        st.audio(audio)    
# To save audio to a file:/可以视为是临时文件，用于语音转文本用
#Open file "audiorecorded.mp3" in binary write mode
        audio_file = open("audiorecorded.mp3", "wb")
# 通过write方法，将麦克风录制的音频audio保存到audiorecorded.mp3中
        audio_file.write(audio)
# 关闭audiorecorded.mp3
        audio_file.close()
except Exception as e:
    # 否则报错Handle the error, e.g., print an error message or return a default text
    print(f"Translation error: {e}")    
    st.write("请先向AI输入语音提问！")  
    st.stop()

#完美播放录制的音频！
st.audio("audiorecorded.mp3", format="audio/mpeg")
#st.audio(audio_bytes, format="audio/mpeg")

#使用SpeechRecognition将录音转文字
recognizer = sr.Recognizer()
audio_file = sr.AudioFile("audiorecorded.mp3")
print(type(audio_file))

with audio_file as source:
  audio_file = recognizer.record(source)
#  audio_file = recognizer.record(source, duration = 5.0)
#  audio_file = recognizer.record(source, offset = 1.0)
  recognizer.recognize_google(audio_data=audio_file)
  print(type(audio_file))
  result = recognizer.recognize_google(audio_data=audio_file)
  print(result)





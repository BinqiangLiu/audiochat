#audio recorder function: https://pypi.org/project/audio-recorder-streamlit/
#python -m pip install --upgrade pip; pip install -r requirements.txt
#python version: 3.10.11
#使用Audio record streamlit（https://pypi.org/project/audio-recorder-streamlit/）（https://github.com/Joooohan/audio-recorder-streamlit）录音
#使用SpeechRecognition 3.10.0（https://pypi.org/project/SpeechRecognition/）将录音转文字
import streamlit as st
#import subprocess
#import openai
import numpy as np
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import ffmpeg
#from langdetect import detect
from gtts import gTTS
# Load environment variables
from dotenv import load_dotenv
import os

st.set_page_config(
    page_title="语音AI随身聊 - 您的随身智能语音助手",
    page_icon=":rocket:",  # You can use Emoji as the page icon
    layout="wide",  # You can set the layout to "wide" or "centered"
)

load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")

in_lang = st.selectbox(
    "请选择您输入语音的语言",
    ("Chinese", "English", "German", "French", "Japanese", "Korean"),
)
if in_lang == "Chinese":
     input_language = "zh-CN"
#elif in_lang == "Chinese Traditional":
#    input_language = "zh-TW"
elif in_lang == "English":
    input_language = "en"
elif in_lang == "German":
    input_language = "de"
elif in_lang == "French":
    input_language = "fr"
elif in_lang == "Japanese":
    input_language = "ja"
elif in_lang == "Korean":
    input_language = "kr"

# Global variable to hold the chat history, initialize with system role
#conversation = [{"role": "system", "content": "You are a helpful assistant."}]

#st.title("语音AI随身聊")
#st.write("---")
#st.header("请用语音向AI智能助手提问！")
st.write("点击下方按钮输入语音（5秒无输入则自动停止）")
audio = audio_recorder(text="红色图标录音中，黑色停止", pause_threshold=5)

audio_listen_cbox = st.checkbox("收听录制的语音", key="audio_cbox")    
if audio_listen_cbox:
   if len(audio) > 0:
        # To play audio in frontend:
        #st.write("↓↓↓播放您输入的语音！")
       st.audio(audio, format="audio/mpeg") 
        # To save audio to a file:/可以视为是临时文件，用于语音转文本用
        #Open file "audiorecorded.mp3" in binary write mode
       audio_file = open("audiorecorded.mp3", "wb")
        # 通过write方法，将麦克风录制的音频audio保存到audiorecorded.mp3中
       audio_file.write(audio)
        # 关闭audiorecorded.mp3（文件已经存好）
       audio_file.close()
       st.write("---")
       
       st.write("Recognizing your audio...wait a while to cheers!")
       #使用SpeechRecognition将录音转文字
       recognizer = sr.Recognizer()
       audio_file = sr.AudioFile("audiorecorded.mp3")
       st.write(type(audio_file))
       st.write("---")
       
       with audio_file as source:
         audio_file = recognizer.record(source)
       #  audio_file = recognizer.record(source, duration = 5.0)
       #  audio_file = recognizer.record(source, offset = 1.0)
         recognizer.recognize_google(audio_data=audio_file)         
         st.write(type(audio_file))
         result = recognizer.recognize_google(audio_data=audio_file, language=input_language )      
         st.write("基于您的输入语言"+input_language+"，识别您的输入为：\n"+result)
       st.write("---")
       
    else:
        #st.write("No audio recorded. Please record your audio first.")
        st.write("未检测到语音。请您先录入语音以向AI助手提问。")
        st.stop()  
#完美播放录制的音频！
#st.audio("audiorecorded.mp3", format="audio/mpeg")
#st.audio(audio_bytes, format="audio/mpeg")

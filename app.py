#使用这个录音模块：https://pypi.org/project/audio-recorder-streamlit/
import streamlit as st
import subprocess
import openai
import numpy as np
from audio_recorder_streamlit import audio_recorder
import numpy as np
import ffmpeg
import av
from langdetect import detect
from gtts import gTTS

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are a helpful assistant."}]

st.title("by Joohan Audio to Chat App")
st.write("---")
st.header("请先向AI提出您的问题！")
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

with open("audiorecorded.mp3", "rb") as sst_audio_file:
    transcript = openai.Audio.transcribe(
        file = sst_audio_file,
        model = "whisper-1",
        response_format="text"        
    )    
st.write("---")    
# Print the transcript of audio input
st.write("你的语音提问（转文字）：\n\n",  transcript)
print("Transcript of your questions:",  transcript)
#因为在openai.Audio.transcribe中使用了response_format="text"，所以直接使用transcript，而不需要使用transcript["text"]

#在将输入语音转文字后，将其作为与ChatGPT聊天的输入（为了保持“记忆”，使用了append）
conversation.append({"role": "user", "content": transcript})
#    conversation.append({"role": "user", "content": transcript["text"]})    
    
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation
)    
#   system_message只提取response的主体部分content
system_message = response["choices"][0]["message"]["content"]

#   为了保持记忆，使用了append ChatGPT system_message (assistant role) back to conversation
conversation.append({"role": "assistant", "content": system_message})

st.write("---")
#将ChatGPT的反馈response输出（复杂格式形式）
print(response)    
print(system_message)    
st.write("ChatGPT的反馈/文字形式（response的完整复杂格式内容）\n\n", response)

st.write("---")
st.write("ChatGPT的反馈/文字形式（response主体内容system_message：\n\n", system_message) 

st.write("---")
# Display the chat history
st.header("你和AI的问答文字记录")

st.write("你的提问（语音转文字）:\n\n " + transcript)
#    st.write("你的提问（语音转文字）: " + transcript["text"])
st.write("---")
st.write("【语音播放AI的回答】")   

language = detect(system_message)

def text_to_speech(text):
    try:
        tts = gTTS(text, lang=language, slow=False)
        tts.save("translationresult.mp3")
#        st.write("Success TTS成功将AI回答转换为语音！")
        return "Success TTS成功将AI回答转换为语音！"    
    except Exception as e:
        # Handle the error, e.g., print an error message or return a default text
        print(f"Translation error: {e}")
        st.write("TTS RESULT ERROR将AI回答转语音失败！")
        return "TTS RESULT ERROR将AI回答转语音失败！"
        st.stop()
        
if system_message is None:
    st.write("请先向AI提问！")    
    st.stop()
else: 
#    st.write("你的提问（AI问答模型中的记录transcript）：\n\n", transcript)
#    st.write(transcript)
#    st.write("---")
#    st.write("AI回答：\n\n")            
    ai_output_audio = text_to_speech(system_message)
    audio_file = open("translationresult.mp3", "rb")
    audio_bytes = audio_file.read()
    st.write("检测到输出语言：", language)
    print(language)
    st.audio("translationresult.mp3")
    st.write("---")
    st.write("ChatGPT的反馈/文字形式（response的完整复杂格式内容）\n\n", response)
    st.write("---")
    st.write("ChatGPT的反馈/文字形式（response主体内容system_message：\n\n", system_message)

#audio recorder function: https://pypi.org/project/audio-recorder-streamlit/
#python -m pip install --upgrade pip; pip install -r requirements.txt
#python version: 3.10.11
#使用Audio record streamlit（https://pypi.org/project/audio-recorder-streamlit/）（https://github.com/Joooohan/audio-recorder-streamlit）录音
#使用SpeechRecognition 3.10.0（https://pypi.org/project/SpeechRecognition/）将录音转文字
#import subprocess
#import openai
#from langdetect import detect
import streamlit as st
import numpy as np
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import ffmpeg
from gtts import gTTS
from langchain import PromptTemplate, LLMChain
from langchain.memory import StreamlitChatMessageHistory
from streamlit_chat import message
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from streamlit.components.v1 import html
from langchain import HuggingFaceHub
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="语音AI随身聊 - 您的随身智能语音助手",
    page_icon=":rocket:",  # You can use Emoji as the page icon
    layout="wide",  # You can set the layout to "wide" or "centered"
)

st.title(":rocket:"+"语音AI随身聊 - 您的随身智能语音助手！")
#st.header("请用语音向AI智能助手提问！")

css_file = "main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

audio_txt_result=""
user_query=""
final_ai_response=""

HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
repo_id = os.environ.get('repo_id')
#repo_id=os.getenv("repo_id")
#openai.api_key = os.getenv("OPENAI_API_KEY")

llm = HuggingFaceHub(repo_id=repo_id,
                     model_kwargs={"min_length":100,
                                   "max_new_tokens":1024, "do_sample":True,
                                   "temperature":0.1,
                                   "top_k":50,
                                   "top_p":0.95, "eos_token_id":49155})

prompt_template = """You are a very helpful AI assistant. Please response to the user's input question with as many details as possible.
Question: {user_question}
Helpufl AI AI Repsonse:
"""  
llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

def text_to_speech(input_language, output_language, text):
    if text is None:
        print("Input empty.")        
    else:
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, slow=False)
        tts.save("translationresult.mp3")
        return trans_text

in_lang = st.selectbox("请选择您输入语音的语言", ("Chinese", "English", "German", "French", "Japanese", "Korean"), key="input_lang")
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
#st.header("请用语音向AI智能助手提问！")

st.write("点击下方按钮输入语音（5秒无输入则自动停止）")
audio = audio_recorder(text="红色图标录音中，黑色停止", pause_threshold=5)
import uuid
file_name = str(uuid.uuid4()) + ".mp3"
st.write("---")
audio_listen_cbox = st.checkbox("收听录制的语音", key="audio_cbox")    
if audio_listen_cbox:
   if audio!=None:
        # To play audio in frontend:
        #st.write("↓↓↓播放您输入的语音！")
       #st.audio(audio, format="audio/mpeg") 
        # To save audio to a file:/可以视为是临时文件，用于语音转文本用
        #Open file "audiorecorded.mp3" in binary write mode
#       audio_file = open("audiorecorded.mp3", "wb")
       audio_file = open(file_name, "wb")
        # 通过write方法，将麦克风录制的音频audio保存到audiorecorded.mp3中
       audio_file.write(audio)
        # 关闭audiorecorded.mp3（文件已经存好）
       audio_file.close()
       
       #使用SpeechRecognition将录音转文字
       recognizer = sr.Recognizer()
       audio_file = sr.AudioFile(file_name)
       #st.write(type(audio_file))
       
       with audio_file as source:
         audio_file = recognizer.record(source)
       #  audio_file = recognizer.record(source, duration = 5.0)
       #  audio_file = recognizer.record(source, offset = 1.0)
         try:
             recognizer.recognize_google(audio_data=audio_file)
             st.audio(audio, format="audio/mpeg") 
             #st.write(type(audio_file))
             with st.spinner("Recognizing your audio...Please wait a while to Cheers!"):                  
               audio_txt_result = recognizer.recognize_google(audio_data=audio_file, language=input_language )
               st.write("基于您的输入语言"+input_language+"，识别您的输入为：\n\n"+audio_txt_result)
#               st.write("基于您的输入语言"+input_language+"，识别您的输入为：\n\n"+audio_txt_result)
#             st.write("---")       
         except Exception as e:
             st.write("检测到语音输入问题（请确保您按照选择的语言正确输入了语音）！")
#             st.stop()    
   else:
        #st.write("No audio recorded. Please record your audio first.")
       st.write("未检测到语音，请您先录入语音以向AI助手提问。")
#       st.stop()  
#st.audio("audiorecorded.mp3", format="audio/mpeg")
#st.audio(audio_bytes, format="audio/mpeg")

ai_response_cbox = st.checkbox("查看AI助手回复", key="ai_cbox")    
if ai_response_cbox:
    user_query = audio_txt_result   
    if user_query !="" and not user_query.strip().isspace() and not user_query == "" and not user_query.strip() == "" and not user_query.isspace():         
      with st.spinner("AI Thinking...Please wait a while to Cheers!"):   
        initial_response=llm_chain.run(user_query)
        temp_ai_response_1=initial_response.partition('<|end|>\n<|user|>\n')[0]
        temp_ai_response_2=temp_ai_response_1.replace('<|end|>\n<|assistant|>\n', '') 
        final_ai_response=temp_ai_response_2.replace('<|end|>\n<|system|>\n', '')         
        st.write("AI Response:")
        st.write(final_ai_response)
    else:        
        st.write("AI助手遇到了错误。请确保您按照选择的语言正确输入了语音！")
#        st.stop()

st.write("---")

ai_response_audio = st.checkbox("语音播放AI助手回复", key="ai_audio_cbox")   
if ai_response_audio:
  out_lang = st.selectbox("请选择希望用来听AI回复的语言", ("English", "Chinese", "German", "French", "Japanese", "Korean"), key="output_lang"
  if out_lang == "English":
    output_language = "en"
  elif out_lang == "Chinese":
    output_language = "zh-CN"
#elif out_lang == "Chinese Traditional":
#    output_language = "zh-TW"
  elif out_lang == "German":
    output_language = "de"
  elif out_lang == "French":
    output_language = "fr"
  elif out_lang == "Japanese":
    output_language = "ja"
  elif out_lang == "Korea":
    output_language = "kr"
  if final_ai_response =="" or final_ai_response.strip().isspace() or final_ai_response == "" or final_ai_response.strip() == ""  or final_ai_response.isspace():
         print("No AI Response Yet.")
  else:
        output_text = text_to_speech(input_language, output_language, final_ai_response)
        audio_file = open("translationresult.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mpeg")

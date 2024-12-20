import streamlit as st
import time
from youtubeqa import Bot
from tools import load_doc_pipeline


# Streamed response emulator
def response_generator(response):
    time.sleep(0.03)
    for word in response.split(" "):
        yield word+ " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "issues" not in st.session_state:
    st.session_state.issues = []

bot = Bot()
with st.container():
    st.markdown("## YoutubeQA")
    url = st.text_input("Indique o link do vídeo para conversar sobre:", "")
    if url:
        try:
            load_doc_pipeline(url)
        except Exception as e:
            st.error('Infelizmente esse vídeo não possui transcrição', icon="🚨")
    st.divider()


@st.fragment
def atualizar_chat(chat_container,prompt=None):
    with chat_container:
        messages = st.session_state.messages

        for i in range(0,len(messages)):
            message = messages[i]       
                                
            if message['role'] == "assistant":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])    

        if prompt:
            with st.chat_message("assistant"):
                with st.spinner(''):
                    response=bot.chat(prompt)
                st.write_stream(response_generator(response))

            st.session_state.messages.append({"role": "assistant", "content": response})


chat_container = st.container(height=400,border=False)
atualizar_chat(chat_container)

if prompt:= st.chat_input("Faça uma pergunta", key="user_input"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    atualizar_chat(chat_container,prompt)
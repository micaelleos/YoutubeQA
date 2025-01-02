import streamlit as st
import time
from youtubeqa import Bot
from tools import load_doc_pipeline
import uuid

# st.html("""
#     <style>
#     .st-emotion-cache-0{
#                 position: sticky;
#                 top: 3.75rem; 
#                 // width: 50%; 
#                 z-index:9999; 
#                 background-color: white}
#     .st-emotion-cache-bm2z3a{
#         width: 100%; 
#     }
#     </style>
# """)

# Streamed response emulator
def response_generator(response):
    time.sleep(0.03)
    for word in response.split(" "):
        yield word+ " "
        time.sleep(0.05)

if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    print(st.session_state.id)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "issues" not in st.session_state:
    st.session_state.issues = []

if "load" not in st.session_state:
    st.session_state.load = []

bot = Bot()
with st.container():
    st.markdown("## YoutubeQA")
    cols = st.columns([0.8,0.2])
    with cols[0]:
        url = st.text_input("Indique o link do vídeo para conversar sobre:", "")
    with cols[1]:
        if st.button("Ok",use_container_width=True):
            tentativas = 0
            while tentativas < 3:
                try:
                    with st.spinner(""):
                        load_doc_pipeline(url)
                        st.session_state["load"] = "Sucesso"
                        bot.load_summary()
                    
                except Exception as e:
                    st.exception(e)
                    st.session_state["load"] = "ERRO"
                
                tentativas += 1
                time.sleep(0.1)
                
    if st.session_state["load"] == "Sucesso":
        st.success("Video carregado com sucesso.")
    elif st.session_state["load"] == "ERRO":
        st.error('Infelizmente esse vídeo não possui transcrição', icon="🚨")


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

with st.container(border=True):
    chat_container = st.container(height=400,border=False)
    atualizar_chat(chat_container)

if prompt:= st.chat_input("Faça uma pergunta", key="user_input"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    atualizar_chat(chat_container,prompt)
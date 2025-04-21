import sys
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.tools import tool
from langchain_core.documents import Document
import streamlit as st
from googleapiclient.discovery import build
import re




# Configurações da API
API_KEY = "AIzaSyA8luSGlOfbwDk7r-Fae6CvulKvNOwp18Q"#os.environ["YOUTUBE_API_KEY"]  # Substitua pela sua chave de API
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
from random import randrange

PERSIST_DIR ='chroma/'

proxys_list = [
'http://zqF7vrzr61igCX4R:74DbvK4zabvQhAL6@geo.g-w.info:10080',
'http://vgH32cWDhIOk2Bw7:PVZ1lCx45zAHtKlG@geo.g-w.info:10080',
'http://nGCApP1Hbhnp8uNc:5uJKM6WGu4ylrTWv@geo.g-w.info:10080',
'http://FCIHpTT8wWaWsUJo:bgEjCLLZoLYPUMgg@geo.g-w.info:10080',
'http://dnJjoIBS7QjO82YW:3lQXC6naPVjOu5er@geo.g-w.info:10080',
'http://bWryHGIo1SbGgMjL:xm4F6X84OWolvGrJ@geo.g-w.info:10080',
'http://Z2hmhG05c6t0Rpsn:9BICzoFvcMoF79Ms@geo.g-w.info:10080',
'http://kuVmSIW7IKK8rv56:qAmb5KDgKIbmKHuH@geo.g-w.info:10080',
'http://ajrbjqj5RdVCBJq6:2olZ7eIsjyAy32c7@geo.g-w.info:10080',
'http://oeM60LpEPpmLkiSZ:lxejKq7KVGovPoZc@geo.g-w.info:10080',
'http://zG0wa4lu2m5a7Imx:xN51BzuBg9f2NYk3@geo.g-w.info:10080',
'http://MJkrWmvEcmTwpTtH:3HJkTQ6hAr8HkHsH@geo.g-w.info:10080',
'http://6wfY0Uv9VUQ8jxBn:agl5FNaD9VIt1t7X@geo.g-w.info:10080',
'http://XF4lKbFuMSyi29o0:mPfwalzcP4lyMJZA@geo.g-w.info:10080',
'http://O37ZFFoiRDe1b9A8:eCmGAy6gZvcYo3wu@geo.g-w.info:10080',
'http://0n7QY373U1u0h3LT:LCpoH8L78aSnptWc@geo.g-w.info:10080',
'http://P9x6vjOsyNOmrbXL:X1t9MFApJGdovjtT@geo.g-w.info:10080',
'http://kwgcKBJ4zwTipstV:KEsvwo7iPMfbGKxM@geo.g-w.info:10080',
'http://mCfiaSjaJmAEisAU:zm2gz0qEvaKLfiTv@geo.g-w.info:10080',
'http://J8d9Anvt86wzmnph:8TjRri18rLMZcSD4@geo.g-w.info:10080',
]

def get_youtube_transcription(video_url):
    proxy = proxys_list[randrange(0,len(proxys_list))]

    ytt_api = YouTubeTranscriptApi(
        proxy_config=GenericProxyConfig(
            http_url=str(proxy),
        )
    )
    print("Proxy used:",proxy)
    # Extrair o ID do vídeo a partir do URL
    video_id = video_url.split("v=")[-1]
    if "&" in video_id:
        video_id = video_id.split("&")[0]
    # Obter a transcrição no idioma especificado
    # all requests done by ytt_api will now be proxied using the defined proxy URLs
    transcript = ytt_api.fetch(video_id,languages=['pt','en']).to_raw_data()

    st.session_state.video_id = video_id

    return transcript


def format_transcript(transcript):
    print("formatação iniciada")
    tempo = 0
    formated_list = []
    frase = ""
    for t in transcript:
      tempo += t['duration']
      frase += t['text']
      if tempo >= 300:
        formated_list.append({"text":frase,"start":round(tempo)})
        tempo = 0
        frase = ""
    print(formated_list)
    return formated_list

def format_doc(docs,link):
    formated_docs = []
    for doc in docs:
      link_tempo = link + "&t=" + str(doc["start"]) + "s"
      document = Document(
              page_content=doc['text'],
              metadata={"source": link_tempo,"time":doc["start"]}
          )
      formated_docs.append(document)
    return formated_docs

@st.cache_resource()
def vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.environ["OPEN_API_KEY"])
    vectorstore = InMemoryVectorStore(embeddings)
    print("caching resource")
    return vectorstore

def load_doc_to_db(doc_splits):
    #embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=os.environ["OPEN_API_KEY"])
    db = vector_store()
    print(db)
    # Add to vectorDB
    ids = db.add_documents(
    documents=doc_splits)

def load_doc_pipeline(link):
    print("inicio")
    transcript = get_youtube_transcription(link)
    print("transcript")
    formated_list = format_transcript(transcript)
    print("formated_list")
    doc_splits = format_doc(formated_list,link)
    print("doc_splits")
    load_doc_to_db(doc_splits)
    print("video loaded")

@st.cache_resource()
def stuff_docs(n=None):
    db = vector_store()
    if not n:
        keys = list(db.store.keys())
    else:
        keys = list(db.store.keys())[:n]
    stuff_doc = []
    for k in keys:
        stuff_doc.append(db.store[k]["text"])
    summary = " ".join(stuff_doc)
    return summary
    
def video_data(video_id):
    # Inicializa o cliente da API do YouTube
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Chama o endpoint videos para obter detalhes do vídeo
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()

    # Verifica se o vídeo foi encontrado
    if "items" not in response or not response["items"]:
        print("Vídeo não encontrado!")
        return

    # Extrai detalhes do vídeo
    video = response["items"][0]
    snippet = video["snippet"]
    statistics = video["statistics"]
    content_details = video["contentDetails"]

    # Exibe os detalhes do vídeo
    dados = f"""
    Canal: {snippet["channelTitle"]}
    Título: {snippet["title"]}
    Descrição: {snippet["description"]}
    Data de publicação: {snippet["publishedAt"]}
    Número de visualizações: {statistics.get("viewCount", "N/A")}
    Número de likes: {statistics.get("likeCount", "N/A")}
    Duração: {content_details["duration"]}
    """
    return dados
  
@tool(response_format="content_and_artifact")
def retriever(query: str):
    """Retrieve information related to a query."""
    print("Ferramenta acionada")
    vectorstore = vector_store()
    retrieved_docs = vectorstore.similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    print(serialized)
    return serialized, retrieved_docs


tools = [retriever]
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.tools import tool
from langchain_core.documents import Document
import streamlit as st
from googleapiclient.discovery import build

# Configurações da API
API_KEY = os.environ["YOUTUBE_API_KEY"]  # Substitua pela sua chave de API
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_youtube_transcription(video_url, language_code=['pt']):
    # Extrair o ID do vídeo a partir do URL
    video_id = video_url.split("v=")[-1]
    if "&" in video_id:
        video_id = video_id.split("&")[0]

    # Guardar id do video para coleta de informações
    if "video_id" not in st.session_state:
        st.session_state.video_id=video_id

    # Obter a transcrição no idioma especificado
    transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=language_code)
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

def load_doc_pipeline(link,language_code='pt'):
    print("inicio")
    transcript = get_youtube_transcription(link)
    print("transcript")
    formated_list = format_transcript(transcript)
    print("formated_list")
    doc_splits = format_doc(formated_list,link)
    print("doc_splits")
    load_doc_to_db(doc_splits)
    stuff_docs()
    print("video loaded")

@st.cache_resource()
def stuff_docs():
    db = vector_store()
    keys = list(db.store.keys())[:4]
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
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import shutil
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, WebVTTFormatter, SRTFormatter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from langchain_core.tools import tool
from langchain_core.documents import Document
from chromadb.config import Settings
import streamlit as st
import tempfile

PERSIST_DIR ='chroma/'

def get_youtube_transcription(video_url, language_code=['pt']):
  # Extrair o ID do vídeo a partir do URL
  video_id = video_url.split("v=")[-1]
  if "&" in video_id:
      video_id = video_id.split("&")[0]
  # Obter a transcrição no idioma especificado
  transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=language_code)
  return transcript


def format_transcript(transcript):
  tempo = 0
  formated_list = []
  frase = ""
  for t in transcript:
    tempo += t['duration']
    frase += t['text']
    if tempo >= 300:
      formated_list.append({"text":frase,"start":tempo})
      tempo = 0
      frase = ""
    formated_list.append({"text":frase,"start":round(tempo)})
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

def load_doc_to_db(doc_splits):
  embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=os.environ["OPEN_API_KEY"])
  db = vector_store()
  # Add to vectorDB
  db.from_documents(
      documents=doc_splits,
      collection_name="rag-chroma",
      embedding=embeddings
  )

def load_doc_pipeline(link,language_code='pt'):
  transcript = get_youtube_transcription(link)
  formated_list = format_transcript(transcript)
  doc_splits = format_doc(formated_list,link)
  load_doc_to_db(doc_splits)
  print("video loaded")

@st.cache_resource()
def vector_store():
  embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.environ["OPEN_API_KEY"])
  persistent_client = chromadb.PersistentClient()
  vectorstore = Chroma(client=persistent_client,
                                  collection_name="rag-chroma",
                                  embedding_function=embeddings,
                                  )
  return vectorstore


def limpar_pasta(caminho_pasta=PERSIST_DIR):

    if not os.path.exists(caminho_pasta):
        print(f"A pasta '{caminho_pasta}' não existe.")
        return
    
    for item in os.listdir(caminho_pasta):
        item_caminho = os.path.join(caminho_pasta, item)
        try:
            if os.path.isfile(item_caminho) or os.path.islink(item_caminho):
                os.unlink(item_caminho)  # Remove arquivos e links simbólicos
            elif os.path.isdir(item_caminho):
                shutil.rmtree(item_caminho)  # Remove diretórios e seus conteúdos
        except Exception as e:
            print(f"Erro ao excluir '{item_caminho}': {e}")
    print(f"A pasta '{caminho_pasta}' foi limpa com sucesso!")


@tool(response_format="content_and_artifact")
def retriever(query: str):
    """Retrieve information related to a query."""
    vectorstore = vector_store()
    retrieved_docs = vectorstore.similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

tools = [retriever]
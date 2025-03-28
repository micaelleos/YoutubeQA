__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import shutil
import chromadb
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter, WebVTTFormatter, SRTFormatter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_core.documents import Document
import streamlit as st

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

def vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.environ["OPEN_API_KEY"])
    persistent_client = chromadb.PersistentClient(path=PERSIST_DIR)
    vectorstore = Chroma(client=persistent_client,
                                    collection_name="rag-chroma",
                                    embedding_function=embeddings,
                                    )
    return vectorstore

def load_doc_to_db(doc_splits):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=os.environ["OPEN_API_KEY"])
    db = vector_store()
    # Add to vectorDB
    db.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    print("load")

def load_doc_pipeline(link,language_code='pt'):
    print("iniciado")
    transcript = get_youtube_transcription(link)
    print(transcript)
    formated_list = format_transcript(transcript)
    print(formated_list)
    doc_splits = format_doc(formated_list,link)
    load_doc_to_db(doc_splits)
    print("video loaded")

@tool(response_format="content_and_artifact")
def retriever(query: str):
    """Retrieve information related to a query."""
    vectorstore = vector_store()
    retrieved_docs = vectorstore.similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    print(serialized)
    return serialized, retrieved_docs

tools = [retriever]
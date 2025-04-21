import os
import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from tools import tools, stuff_docs, video_data
from langchain_core.messages import AIMessage
from prompt import prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

@st.cache_resource()
def memory():
    memory = MemorySaver() 
    return memory

class Bot():
    def __init__(self):
        self.OPENAI_API_KEY=os.environ["OPEN_API_KEY"]

        self.llm = ChatOpenAI(model="gpt-4o",api_key=self.OPENAI_API_KEY)
        self.memory = memory()
        self.tools = tools
        self.agent_executor = create_react_agent(self.llm, self.tools, checkpointer=self.memory, state_modifier=prompt)

        self.config = {"configurable": {"thread_id": "def234"}}

    def chat(self,query:str):
        menssage = None
        for event in self.agent_executor.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="values",
            config=self.config,
        ):
            event["messages"][-1].pretty_print()
            if isinstance(event["messages"][-1], AIMessage):
                menssage = event["messages"][-1]
        return menssage.content
    
    def load_init(self):
        text = stuff_docs(4)
        data = video_data(st.session_state.video_id)
        stuff_summary = self.video_summary()
        summary = f""" Seguem a seguir dados do vídeo, e seu início:
        #### Dados:
        {data}

        #### 15 primeiros minutos do vídeo, para entendimento de contexto:
        {text}

        #### Segue o resumo do vídeo:
        {stuff_summary}
        """
        self.agent_executor.invoke(input={"messages":[{"role":"assistant","content":summary}]},config=self.config)

    def video_summary(self):
        """ Utilize essa ferramenta para ter acesso ao resumo do vídeo completo"""
        text = stuff_docs()
        
        llm = ChatOpenAI(model="gpt-3.5-turbo",api_key=os.environ["OPEN_API_KEY"])
        map_prompt = ChatPromptTemplate.from_messages(
        [("human", "Escreva um resumo consiso, com a squematização de timestamp do vídeo, do seguinte:\\n\\n{context}")] 
        )

        map_chain = map_prompt | llm | StrOutputParser()

        stuff_summary = ""

        if len(text) > 4000:
            for s in range(2000,2000,len(text)):
                stuff_summary =+ map_chain.invoke({"context":text[s-2000:s]})

            stuff_summary = map_chain.invoke({"context":stuff_summary})

        else:
            stuff_summary = map_chain.invoke({"context":text})

        print("Aqui---------",len(text),stuff_summary)

        return stuff_summary


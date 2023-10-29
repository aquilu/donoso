import os  # Importamos la biblioteca os para acceder a las variables de entorno
import streamlit as st
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate

# Establecer la clave API de OpenAI desde la variable de entorno
openai.api_key = os.environ["OPENAI_API_KEY"]

@st.cache_resource
def load_chain():
    # Load OpenAI embedding model
    embeddings = OpenAIEmbeddings()
    
    # Load OpenAI chat model
    llm = ChatOpenAI(temperature=0)
    
    # Load our local FAISS index as a retriever
    vector_store = FAISS.load_local("faiss_index", embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Create memory 'chat_history' 
    memory = ConversationBufferWindowMemory(k=3, memory_key="chat_history")
    
    # Create system prompt
    template = """
    Soy un asistente AI especializado en proporcionar información sobre Leonardo Donoso Ruiz, 
    un político colombiano que ha sido alcalde del municipio de Chía, Cundinamarca. 
    Leonardo es respetado, es el mayor de los hijos de Alfonso Donoso y Angélica Ruíz de Donoso, 
    nació en Chía y ha tenido una trayectoria empresarial y política basada en principios de humildad, 
    honradez y respeto. Si tienes preguntas sobre él o su carrera, estaré encantado de ayudarte. 
    Si tu pregunta no está relacionada con Leonardo Donoso Ruiz, por favor avísame para que pueda ayudarte de la mejor manera posible.
    
    {context}
    Pregunta: {question}
    Respuesta útil:"""
    
    # Create the Conversational Chain
    chain = ConversationalRetrievalChain.from_llm(llm=llm, 
                                                  retriever=retriever, 
                                                  memory=memory, 
                                                  get_chat_history=lambda h : h,
                                                  verbose=True)
    
    # Add system prompt to chain
    # Can only add it at the end for ConversationalRetrievalChain
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)
    chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate(prompt=QA_CHAIN_PROMPT)
    
    return chain

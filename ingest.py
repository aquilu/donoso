import os
import openai
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Obtener la clave API de OpenAI desde las variables de entorno del sistema
openai.api_key = os.environ["OPENAI_API_KEY"]

# Load the content located in 'donoso_content/donoso.md'
loader = UnstructuredMarkdownLoader("donoso_content/donoso.md")  # Ruta actualizada
documents = loader.load()

# Split the content into smaller chunks
markdown_splitter = RecursiveCharacterTextSplitter(
    separators=["#", "##", "###", "\\n\\n", "\\n", "."],
    chunk_size=1500,
    chunk_overlap=100)
docs = markdown_splitter.split_documents(documents)

# Initialize OpenAI embedding model
embeddings = OpenAIEmbeddings()

# Convert all chunks into vectors embeddings using OpenAI embedding model
# Store all vectors in FAISS index and save to local folder 'faiss_index'
db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index")

print('Local FAISS index has been successfully saved.')
import os
import sys
from typing import List
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI client
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except AttributeError:
    print("Error: GOOGLE_API_KEY not found. Please set it in your .env file.")
    sys.exit(1)

# --- 1. Data Loading and Splitting ---
loader = TextLoader("data/business_info.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
texts = [doc.page_content for doc in docs]

print(f"Split document into {len(docs)} chunks.")

# --- 2. Create Embeddings ---
model = 'models/embedding-001'
embeddings = genai.embed_content(model=model,
                                 content=texts,
                                 task_type="retrieval_document")['embedding']

print(f"Successfully created {len(embeddings)} embeddings.")

# --- 3. Store in ChromaDB ---
client = chromadb.PersistentClient(path="./chroma_db")

# Delete the collection if it exists, to ensure a fresh start
if "wine_business_knowledge" in [c.name for c in client.list_collections()]:
    client.delete_collection(name="wine_business_knowledge")
    print("Existing collection 'wine_business_knowledge' deleted.")

collection = client.create_collection("wine_business_knowledge")

collection.add(
    ids=[f"doc_{i}" for i in range(len(texts))],
    embeddings=embeddings,
    documents=texts,
    metadatas=[{'source': 'business_info.txt'} for _ in texts]
)

print(f"\n✅ Successfully created and populated the vector store with {collection.count()} documents.")
print("You can now run app.py to chat with your knowledge base.")

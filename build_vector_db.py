"""
build_vector_db.py

This script:

1. Loads all PDFs from the data folder.
2. Splits them into chunks.
3. Creates embeddings using Google Gemini.
4. Stores the embeddings inside a FAISS Vector Database.

Run this script only once unless the PDFs change.
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.vectorstores import FAISS

# ----------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise Exception("GOOGLE_API_KEY not found in .env")

# ----------------------------------------------------
# Folder Paths
# ----------------------------------------------------

PDF_FOLDER = "data"

VECTOR_DB_PATH = "vector_db"

# ----------------------------------------------------
# Step 1 : Load PDFs
# ----------------------------------------------------

print("=" * 60)
print("Loading PDF Documents")
print("=" * 60)

loader = PyPDFDirectoryLoader(PDF_FOLDER)

documents = loader.load()

print(f"\nNumber of pages loaded : {len(documents)}")

# ----------------------------------------------------
# Step 2 : Display Loaded Pages
# ----------------------------------------------------

for i, doc in enumerate(documents[:5]):

    print("\n-------------------------------------")
    print(f"Page : {i+1}")

    print("Source :")

    print(doc.metadata["source"])

    print("Page Number :")

    print(doc.metadata["page"] + 1)

# ----------------------------------------------------
# Step 3 : Split Documents
# ----------------------------------------------------

print("\n")
print("=" * 60)
print("Splitting Documents")
print("=" * 60)

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=100

)

chunks = text_splitter.split_documents(documents)

print(f"\nTotal Chunks Created : {len(chunks)}")

# ----------------------------------------------------
# Step 4 : Display Sample Chunks
# ----------------------------------------------------

print("\nSample Chunks\n")

for i in range(min(3, len(chunks))):

    print("-" * 60)

    print(chunks[i].page_content[:400])

# ----------------------------------------------------
# Step 5 : Create Embeddings
# ----------------------------------------------------

print("\n")
print("=" * 60)
print("Creating Embeddings")
print("=" * 60)

embedding_model = GoogleGenerativeAIEmbeddings(

    model="models/embedding-001"

)

# ----------------------------------------------------
# Step 6 : Build Vector Database
# ----------------------------------------------------

print("\nCreating FAISS Index...")

vector_db = FAISS.from_documents(

    documents=chunks,

    embedding=embedding_model

)

# ----------------------------------------------------
# Step 7 : Save Vector Database
# ----------------------------------------------------

vector_db.save_local(VECTOR_DB_PATH)

print("\nVector Database Saved Successfully")

print(VECTOR_DB_PATH)

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

print("\n")
print("=" * 60)

print("Summary")

print("=" * 60)

print(f"PDF Pages      : {len(documents)}")

print(f"Chunks Created : {len(chunks)}")

print(f"Chunk Size     : 500")

print(f"Chunk Overlap  : 100")

print(f"Vector DB Path : {VECTOR_DB_PATH}")

print("\nCompleted Successfully.")

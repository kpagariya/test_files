

import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

VECTOR_DB_PATH = "vector_db"

TOP_K = 4

# ----------------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------------

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found.")

# ----------------------------------------------------------
# Create Embedding Model
# ----------------------------------------------------------

print("=" * 60)
print("Loading Embedding Model")
print("=" * 60)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

print("Embedding model loaded.\n")

# ----------------------------------------------------------
# Load FAISS Database
# ----------------------------------------------------------

print("=" * 60)
print("Loading FAISS Vector Database")
print("=" * 60)

vector_db = FAISS.load_local(
    folder_path=VECTOR_DB_PATH,
    embeddings=embeddings,
    allow_dangerous_deserialization=True,
)

print("Vector Database Loaded Successfully.\n")

# ----------------------------------------------------------
# Create Retriever
# ----------------------------------------------------------

retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": TOP_K},
)

print(f"Retriever Ready (Top K = {TOP_K})")

print("\nType 'exit' to quit.\n")

# ----------------------------------------------------------
# Interactive Loop
# ----------------------------------------------------------

while True:

    print("=" * 70)

    question = input("Question : ").strip()

    if question.lower() == "exit":
        print("\nGood Bye")
        break

    print("\nSearching...\n")

    docs = retriever.invoke(question)

    print("=" * 70)
    print(f"Retrieved {len(docs)} document(s)")
    print("=" * 70)

    for i, doc in enumerate(docs, start=1):

        metadata = doc.metadata

        source = metadata.get("source", "Unknown")

        page = metadata.get("page", "NA")

        print(f"\nDocument #{i}")

        print("-" * 60)

        print(f"Source : {source}")

        if page != "NA":
            print(f"Page   : {page + 1}")

        print("\nContent\n")

        print(doc.page_content)

        print()

    print("=" * 70)

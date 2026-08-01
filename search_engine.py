"""
===========================================================
search_engine.py
===========================================================

Purpose:
--------
Search the FAISS Vector Database using one or more queries.

Input:
------
[
    "Admission process",
    "Student enrollment",
    "Registration procedure"
]

Output:
-------
{
    "Admission process": [Document, Document, ...],
    "Student enrollment": [Document, Document, ...],
    "Registration procedure": [Document, Document, ...]
}

Author : ChatGPT Advanced RAG Course
"""

import os
from typing import Dict, List

from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class SearchEngine:

    def __init__(
        self,
        vector_db_path: str = "vector_db",
        top_k: int = 4
    ):
        """
        Initialize Search Engine
        """

        load_dotenv()

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found.")

        self.top_k = top_k

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        self.vector_db = FAISS.load_local(
            folder_path=vector_db_path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )

        self.retriever = self.vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": self.top_k
            }
        )

    # ----------------------------------------------------

    def search(self, query: str) -> List[Document]:
        """
        Search a single query.
        """

        return self.retriever.invoke(query)

    # ----------------------------------------------------

    def search_multiple(
        self,
        queries: List[str]
    ) -> Dict[str, List[Document]]:
        """
        Search multiple queries.

        Returns

        {
            query1 : [docs],
            query2 : [docs]
        }
        """

        results = {}

        for query in queries:

            docs = self.search(query)

            results[query] = docs

        return results

    # ----------------------------------------------------

    @staticmethod
    def print_results(results: Dict[str, List[Document]]):

        print("\n")
        print("=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)

        for query, docs in results.items():

            print("\n")
            print("-" * 80)
            print(f"Query : {query}")
            print("-" * 80)

            for index, doc in enumerate(docs, start=1):

                source = doc.metadata.get("source", "Unknown")

                page = doc.metadata.get("page", "NA")

                print(f"\nDocument {index}")

                print(f"Source : {source}")

                if page != "NA":
                    print(f"Page   : {page + 1}")

                print()

                preview = doc.page_content[:250]

                print(preview)

                print("...")


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    queries = [

        "Admission process",

        "Student enrollment",

        "Registration procedure",

        "Application process"

    ]

    engine = SearchEngine()

    results = engine.search_multiple(queries)

    engine.print_results(results)

"""
===========================================================
duplicate_remover.py
===========================================================

Purpose
-------
Remove duplicate documents retrieved from multiple queries.

Input
-----
{
    "Query 1": [(Document, score), ...],
    "Query 2": [(Document, score), ...]
}

Output
------
[
    (Document, score),
    (Document, score),
    ...
]

Author : ChatGPT Advanced RAG Course
"""

from typing import Dict, List, Tuple

from langchain_core.documents import Document


class DuplicateRemover:

    @staticmethod
    def remove_duplicates(
        search_results: Dict[str, List[Tuple[Document, float]]]
    ) -> List[Tuple[Document, float]]:
        """
        Remove duplicate documents.

        Duplicate is identified using:
        Source + Page + Content

        If duplicate appears multiple times,
        keep the one having the lowest distance score.
        """

        unique_docs = {}

        for query, results in search_results.items():

            for doc, score in results:

                source = doc.metadata.get("source", "")
                page = doc.metadata.get("page", -1)

                key = (
                    source,
                    page,
                    doc.page_content.strip()
                )

                # First occurrence
                if key not in unique_docs:
                    unique_docs[key] = (doc, score)

                else:
                    # Keep the better match
                    _, existing_score = unique_docs[key]

                    if score < existing_score:
                        unique_docs[key] = (doc, score)

        # Sort by score (lower distance = better)
        final_docs = sorted(
            unique_docs.values(),
            key=lambda x: x[1]
        )

        return final_docs

    # --------------------------------------------------

    @staticmethod
    def print_results(
        documents: List[Tuple[Document, float]]
    ):

        print("\n")
        print("=" * 80)
        print("UNIQUE DOCUMENTS")
        print("=" * 80)

        for rank, (doc, score) in enumerate(documents, start=1):

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "NA")

            print("\n")
            print("-" * 80)
            print(f"Rank : {rank}")
            print(f"Distance Score : {score:.4f}")
            print(f"Source : {source}")

            if page != "NA":
                print(f"Page : {page + 1}")

            print()

            print(doc.page_content[:250])

            print("...")

        print("\n")
        print("=" * 80)
        print(f"Total Unique Documents : {len(documents)}")
        print("=" * 80)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    print(
        "Run this file through main.py after "
        "search_engine.py generates results."
    )

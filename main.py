"""
===========================================================
Manual Multi Query Retriever
===========================================================
"""

from query_generator import QueryGenerator
from search_engine import SearchEngine
from duplicate_remover import DuplicateRemover
from answer_generator import AnswerGenerator


def main():

    print("=" * 70)
    print("MANUAL MULTI QUERY RETRIEVER")
    print("=" * 70)

    question = input("\nQuestion : ")

    # ----------------------------------------
    # Step 1
    # ----------------------------------------

    print("\nSTEP 1 : Query Generation\n")

    generator = QueryGenerator()

    queries = generator.generate(question)

    for i, query in enumerate(queries, start=1):
        print(f"{i}. {query}")

    # ----------------------------------------
    # Step 2
    # ----------------------------------------

    print("\nSTEP 2 : Searching Vector Database\n")

    engine = SearchEngine()

    results = engine.search_multiple(queries)

    engine.print_results(results)

    # ----------------------------------------
    # Step 3
    # ----------------------------------------

    print("\nSTEP 3 : Removing Duplicates\n")

    duplicate_result = DuplicateRemover.remove_duplicates(results)

    unique_docs = duplicate_result["documents"]

    print(f"Total Retrieved     : {duplicate_result['total_documents']}")
    print(f"Unique Documents    : {duplicate_result['unique_documents']}")
    print(f"Duplicates Removed  : {duplicate_result['duplicate_documents']}")

    DuplicateRemover.print_results(unique_docs)

    # ----------------------------------------
    # Step 4
    # ----------------------------------------

    print("\nSTEP 4 : Generating Final Answer\n")

    answer_generator = AnswerGenerator()

    answer = answer_generator.generate(
        question=question,
        documents=unique_docs
    )

    print("=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(answer)


if __name__ == "__main__":
    main()

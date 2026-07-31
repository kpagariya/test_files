"""
===========================================================
query_generator.py
===========================================================

Purpose:
--------
Generate multiple search queries from one user question.

Example

Input:
------
How do students join the university?

Output:
-------
1. Explain the admission process.
2. How can a student enroll?
3. What is the registration process?
4. How do I apply for admission?
5. Orientation process for new students.

Author : ChatGPT Advanced RAG Course
"""

from typing import List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI


class QueryGenerator:

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.2,
    ):

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert search query generator.

Your job is to generate multiple search queries
that retrieve different but relevant information.

Rules:

1. Return EXACTLY five queries.

2. Each query should be different.

3. Preserve the original meaning.

4. Use synonyms whenever possible.

5. Keep every query short.

6. Return only the queries.

7. One query per line.

Do not number them.

Do not explain anything.
                    """,
                ),
                (
                    "human",
                    "{question}",
                ),
            ]
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    # ----------------------------------------------------

    def generate(self, question: str) -> List[str]:

        response = self.chain.invoke(
            {
                "question": question
            }
        )

        queries = []

        for line in response.split("\n"):

            line = line.strip()

            if not line:
                continue

            # remove bullets

            line = line.lstrip("-")

            line = line.lstrip("*")

            line = line.strip()

            queries.append(line)

        # Remove duplicates

        unique_queries = []

        seen = set()

        for query in queries:

            key = query.lower()

            if key not in seen:

                seen.add(key)

                unique_queries.append(query)

        return unique_queries


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    generator = QueryGenerator()

    question = input("Question : ")

    generated_queries = generator.generate(question)

    print()

    print("=" * 60)

    print("Generated Queries")

    print("=" * 60)

    for i, q in enumerate(generated_queries, start=1):

        print(f"{i}. {q}")

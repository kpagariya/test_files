"""
===========================================================
answer_generator.py
===========================================================
Generate the final answer using the retrieved documents.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from prompts import ANSWER_GENERATION_PROMPT


class AnswerGenerator:

    def __init__(
        self,
        model_name="gemini-2.5-flash",
        temperature=0.2
    ):

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature
        )

        self.prompt = ChatPromptTemplate.from_template(
            ANSWER_GENERATION_PROMPT
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    # ----------------------------------------------------

    @staticmethod
    def build_context(documents):

        context = []

        for i, (doc, score) in enumerate(documents, start=1):

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", 0)

            context.append(
                f"""
Document {i}

Source : {source}
Page   : {page+1}

{doc.page_content}
"""
            )

        return "\n\n".join(context)

    # ----------------------------------------------------

    def generate(
        self,
        question,
        documents
    ):

        context = self.build_context(documents)

        answer = self.chain.invoke(
            {
                "question": question,
                "context": context
            }
        )

        return answer

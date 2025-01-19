
import sys
import os

# Add the `src` directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from rag_app.get_chroma_db import get_chroma_db

PROMPT_TEMPLATE = """
Answer the question based only on the following context:
<context>
{context}
</context>

---

Answer the question based on the above context: {question}
"""

@dataclass
class QueryResponse:
    query_text: str
    sources: List[str]
    response_text: str

def query_rag(query_text:str) -> QueryResponse:
    db = get_chroma_db()

    # Search the DB
    results = db.similarity_search_with_score(query_text,k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    llm = OllamaLLM(model="llama3.2")
    response = llm.invoke(prompt)
  

    sources = [doc.metadata.get("id",None) for doc,_score in results]
    print(f"Response: {response}\nSources: {sources}")

    return QueryResponse(
        query_text = query_text,
        sources = sources,
        response_text = response
            )

if __name__ == "__main__":
    query_rag("tell me something about the Account Management and Support")